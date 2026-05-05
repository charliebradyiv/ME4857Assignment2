#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from std_msgs.msg import Bool, String, Float32
from std_srvs.srv import Trigger
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from sr_interfaces.action import NavigateToWaypoint

import py_trees
import time
import math


# ─────────────────────────────────────────────
# Behaviours
# ─────────────────────────────────────────────

class WaitForSensors(py_trees.behaviour.Behaviour):
    """
    Blocks the BT from starting until all required sensor nodes have
    published at least one message. This prevents the robot from acting
    on uninitialised state (e.g. fire_too_close defaulting to False
    before fire_safety.py has published anything).

    Waits for:
      - /fire_safe  (fire_safety.py must be running)
      - /odom       (diff_drive_controller must be active)
      - /scan       (LiDAR bridge must be active)
    """

    def __init__(self, node):
        super().__init__('WaitForSensors')
        self.node = node

    def update(self):
        ready = (
            self.node.fire_safe_received and
            self.node.odom_received and
            self.node.scan_received
        )

        if ready:
            self.node.get_logger().info('All sensors ready — starting mission')
            return py_trees.common.Status.SUCCESS

        waiting_for = []
        if not self.node.fire_safe_received:
            waiting_for.append('fire_safety (/fire_safe)')
        if not self.node.odom_received:
            waiting_for.append('odometry (/odom)')
        if not self.node.scan_received:
            waiting_for.append('lidar (/scan)')

        self.node.get_logger().info(
            f'Waiting for: {", ".join(waiting_for)}',
            throttle_duration_sec=2.0
        )
        return py_trees.common.Status.RUNNING


class BatteryOK(py_trees.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__('BatteryOK')
        self.node = node

    def update(self):
        if self.node.battery_low:
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.SUCCESS


class FireSafe(py_trees.behaviour.Behaviour):
    """
    Reads fire safety status from /fire_safe topic published by fire_safety.py.
    fire_safety.py owns all fire distance logic — this just reads the result.
    """
    def __init__(self, node):
        super().__init__('FireSafe')
        self.node = node

    def update(self):
        if self.node.fire_too_close:
            self.node.get_logger().warn('Fire safety: too close to fire!')
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.SUCCESS


class RetreatFromFire(py_trees.behaviour.Behaviour):
    """
    Drives the robot away from the fire when FireSafe fails.
    Fire coordinates are kept here as constants — fire_safety.py owns
    the detection logic, but retreat direction still needs the position.
    """
    FIRE_X   = -14.2
    FIRE_Y   = 10.8
    MIN_DIST = 3.0
    BUFFER   = 0.5

    def __init__(self, node):
        super().__init__('RetreatFromFire')
        self.node = node

    def update(self):
        dx = self.node.robot_x - self.FIRE_X
        dy = self.node.robot_y - self.FIRE_Y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist >= self.MIN_DIST + self.BUFFER:
            self.node.cmd_vel_pub.publish(Twist())
            self.node.get_logger().info(
                f'Fire retreat complete — {dist:.2f}m from fire'
            )
            return py_trees.common.Status.SUCCESS

        away_angle = math.atan2(dy, dx)
        heading_error = self.node.angle_diff(away_angle, self.node.robot_yaw)

        twist = Twist()
        if abs(heading_error) > 0.4:
            twist.linear.x = 0.0
            twist.angular.z = max(-0.6, min(0.6, heading_error * 1.2))
        else:
            twist.linear.x = 0.3
            twist.angular.z = heading_error * 0.5

        self.node.cmd_vel_pub.publish(twist)
        self.node.get_logger().warn(
            f'Retreating from fire — {dist:.2f}m of {self.MIN_DIST}m',
            throttle_duration_sec=1.0
        )
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        self.node.cmd_vel_pub.publish(Twist())


class ScanEnvironment(py_trees.behaviour.Behaviour):
    """
    Rotates 360 degrees at startup and records the best bearing for each colour.
    Scan progress stored on node so interruptions don't reset it.
    """

    FULL_ROTATION = 2.0 * math.pi
    SCAN_SPEED    = 0.3
    HALF_FOV      = 0.52  # ~30 degree half-FOV

    def __init__(self, node):
        super().__init__('ScanEnvironment')
        self.node = node
        self._last_yaw = None

    def initialise(self):
        if not hasattr(self.node, '_scan_rotated'):
            self.node._scan_rotated    = 0.0
            self.node._scan_best_areas = {}
            self.node.colour_bearings  = {}
            self.node.get_logger().info('ScanEnvironment: starting 360 degree scan')
        else:
            self.node.get_logger().info(
                f'ScanEnvironment: resuming at '
                f'{math.degrees(self.node._scan_rotated):.0f} deg'
            )
        self._last_yaw = self.node.robot_yaw

    def update(self):
        current_yaw = self.node.robot_yaw
        delta = self.node.angle_diff(current_yaw, self._last_yaw)
        self.node._scan_rotated += abs(delta)
        self._last_yaw = current_yaw

        if self.node.colour_visible and self.node.detected_colour != 'none':
            colour = self.node.detected_colour
            area   = self.node.colour_area
            if area > self.node._scan_best_areas.get(colour, 0.0):
                self.node._scan_best_areas[colour] = area
                bearing = current_yaw - self.node.colour_offset_x * self.HALF_FOV
                self.node.colour_bearings[colour] = bearing
                self.node.get_logger().info(
                    f'Scan: {colour} at yaw={math.degrees(current_yaw):.1f} deg  '
                    f'bearing={math.degrees(bearing):.1f} deg  area={area:.0f}'
                )

        if self.node._scan_rotated >= self.FULL_ROTATION:
            self.node.cmd_vel_pub.publish(Twist())
            del self.node._scan_rotated
            del self.node._scan_best_areas
            self.node.get_logger().info(
                f'Scan complete. Found: {list(self.node.colour_bearings.keys())}'
            )
            return py_trees.common.Status.SUCCESS

        twist = Twist()
        twist.angular.z = self.SCAN_SPEED
        self.node.cmd_vel_pub.publish(twist)
        self.node.get_logger().info(
            f'Scanning... {math.degrees(self.node._scan_rotated):.0f} / 360 deg',
            throttle_duration_sec=2.0
        )
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        # Do NOT delete _scan_rotated — preserve progress on interruption
        self.node.cmd_vel_pub.publish(Twist())


class NavigateToVerified(py_trees.behaviour.Behaviour):
    """
    Hybrid navigation: waypoint coordinates + camera colour verification.

    Phase 1 — NAVIGATE:
      Sends a goal to navigate_to_server with the target waypoint name.
      navigate_to_server drives using hardcoded coordinates with LiDAR
      obstacle avoidance. Returns SUCCESS when within stop_distance.

    Phase 2 — VERIFY:
      Once the waypoint is reached, the camera confirms the expected colour
      is visible. Rotates slowly to search if not immediately in view.
      Times out after verify_timeout seconds and proceeds anyway.
    """

    def __init__(self, name, node, target_name, expected_colour,
                 stop_distance=1.0, verify_timeout=15.0):
        super().__init__(name)
        self.node            = node
        self.target_name     = target_name
        self.expected_colour = expected_colour
        self.stop_distance   = stop_distance
        self.verify_timeout  = verify_timeout

        self._client       = ActionClient(node, NavigateToWaypoint, 'navigate_to_waypoint')
        self._goal_handle  = None
        self._result       = None
        self._sent         = False
        self._phase        = 'NAVIGATE'
        self._verify_start = None

    def initialise(self):
        self._sent         = False
        self._goal_handle  = None
        self._result       = None
        self._phase        = 'NAVIGATE'
        self._verify_start = None
        self.node.get_logger().info(
            f'NavigateToVerified [{self.target_name}]: navigating to waypoint'
        )

    def update(self):

        # ── Phase 1: NAVIGATE ───────────────────────────────────────────────
        if self._phase == 'NAVIGATE':
            if not self._sent:
                if not self._client.wait_for_server(timeout_sec=2.0):
                    self.node.get_logger().error('navigate_to_waypoint server unavailable')
                    return py_trees.common.Status.FAILURE

                goal = NavigateToWaypoint.Goal()
                goal.target_name   = self.target_name
                goal.stop_distance = self.stop_distance

                self._future = self._client.send_goal_async(
                    goal,
                    feedback_callback=self._feedback_cb
                )
                self._sent = True
                self._future.add_done_callback(self._goal_response_cb)
                return py_trees.common.Status.RUNNING

            rclpy.spin_once(self.node, timeout_sec=0.0)

            if self._result is None:
                return py_trees.common.Status.RUNNING

            if not self._result.success:
                self.node.get_logger().error(
                    f'Navigation to {self.target_name} failed'
                )
                return py_trees.common.Status.FAILURE

            self.node.get_logger().info(
                f'Reached {self.target_name} waypoint — verifying with camera'
            )
            self._phase        = 'VERIFY'
            self._verify_start = time.time()

        # ── Phase 2: VERIFY ─────────────────────────────────────────────────
        if self._phase == 'VERIFY':
            if (self.node.colour_visible and
                    self.node.detected_colour == self.expected_colour):
                self.node.cmd_vel_pub.publish(Twist())
                self.node.get_logger().info(
                    f'Verified {self.expected_colour} at {self.target_name}'
                )
                return py_trees.common.Status.SUCCESS

            if time.time() - self._verify_start > self.verify_timeout:
                self.node.cmd_vel_pub.publish(Twist())
                self.node.get_logger().warn(
                    f'Verify timeout at {self.target_name} — '
                    f'camera sees {self.node.detected_colour}, '
                    f'expected {self.expected_colour}. Proceeding anyway.'
                )
                return py_trees.common.Status.SUCCESS

            twist = Twist()
            if (self.node.colour_visible and
                    self.node.detected_colour == self.expected_colour):
                twist.angular.z = -0.4 * self.node.colour_offset_x
            else:
                twist.angular.z = 0.25

            self.node.cmd_vel_pub.publish(twist)
            self.node.get_logger().info(
                f'Verifying {self.expected_colour} at {self.target_name} — '
                f'sees: {self.node.detected_colour}',
                throttle_duration_sec=1.0
            )
            return py_trees.common.Status.RUNNING

        return py_trees.common.Status.FAILURE

    def _feedback_cb(self, feedback):
        dist = feedback.feedback.distance_remaining
        self.node.get_logger().info(
            f'Navigating to {self.target_name}: {dist:.2f}m remaining',
            throttle_duration_sec=2.0
        )

    def _goal_response_cb(self, future):
        self._goal_handle = future.result()
        if self._goal_handle.accepted:
            result_future = self._goal_handle.get_result_async()
            result_future.add_done_callback(self._result_cb)
        else:
            self.node.get_logger().error(f'Goal to {self.target_name} rejected')

    def _result_cb(self, future):
        self._result = future.result().result

    def terminate(self, new_status):
        self.node.cmd_vel_pub.publish(Twist())
        if self._goal_handle is not None:
            self._goal_handle.cancel_goal_async()


class WaitSeconds(py_trees.behaviour.Behaviour):
    def __init__(self, name, seconds):
        super().__init__(name)
        self.seconds = seconds
        self._start = None

    def initialise(self):
        self._start = time.time()

    def update(self):
        if time.time() - self._start >= self.seconds:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.RUNNING


class PublishSurvivorTF(py_trees.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__('PublishSurvivorTF')
        self.node = node
        self._called = False

    def initialise(self):
        self._called = False

    def update(self):
        if not self._called:
            if not self.node.survivor_tf_client.wait_for_service(timeout_sec=2.0):
                self.node.get_logger().error('publish_survivor_tf service not available')
                return py_trees.common.Status.FAILURE
            future = self.node.survivor_tf_client.call_async(Trigger.Request())
            rclpy.spin_until_future_complete(self.node, future, timeout_sec=2.0)
            self._called = True
            self.node.get_logger().info('Survivor TF service called')
        return py_trees.common.Status.SUCCESS


class RotateRobot(py_trees.behaviour.Behaviour):
    def __init__(self, name, node, degrees):
        super().__init__(name)
        self.node = node
        self.degrees = degrees
        self._start = None

    def initialise(self):
        self._start = time.time()

    def update(self):
        duration = abs(self.degrees) / 17.0
        if time.time() - self._start >= duration:
            self.node.cmd_vel_pub.publish(Twist())
            return py_trees.common.Status.SUCCESS
        twist = Twist()
        twist.angular.z = 0.3 if self.degrees > 0 else -0.3
        self.node.cmd_vel_pub.publish(twist)
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        self.node.cmd_vel_pub.publish(Twist())


class WaitForCharge(py_trees.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__('WaitForCharge')
        self.node = node

    def update(self):
        if not self.node.battery_low:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.RUNNING


class StopAndWait(py_trees.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__('StopAndWait')
        self.node = node

    def initialise(self):
        self.node.cmd_vel_pub.publish(Twist())

    def update(self):
        return py_trees.common.Status.RUNNING


class MarkTaskDone(py_trees.behaviour.Behaviour):
    def __init__(self, name, node, flag_name):
        super().__init__(name)
        self.node = node
        self.flag_name = flag_name

    def update(self):
        setattr(self.node, self.flag_name, True)
        self.node.get_logger().info(f'{self.flag_name} = True')
        return py_trees.common.Status.SUCCESS


class TaskAlreadyDone(py_trees.behaviour.Behaviour):
    def __init__(self, name, node, flag_name):
        super().__init__(name)
        self.node = node
        self.flag_name = flag_name

    def update(self):
        if getattr(self.node, self.flag_name, False):
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


# ─────────────────────────────────────────────
# BT Runner Node
# ─────────────────────────────────────────────

class BTRunner(Node):
    def __init__(self):
        super().__init__('bt_runner')

        # Robot pose
        self.robot_x   = 0.0
        self.robot_y   = 0.0
        self.robot_yaw = 0.0

        # Fire safety — driven by /fire_safe from fire_safety.py
        # fire_safety.py owns all distance logic. bt_runner just reads the flag.
        self.fire_too_close = False

        # Sensor ready flags — WaitForSensors blocks until all True
        self.fire_safe_received = False
        self.odom_received      = False
        self.scan_received      = False

        # Battery
        self.battery_low = False

        # Camera state
        self.detected_colour = 'none'
        self.colour_visible  = False
        self.colour_offset_x = 0.0
        self.colour_area     = 0.0

        # LiDAR state
        self.front_obstacle_distance = float('inf')

        # Bearings from startup scan
        self.colour_bearings = {}

        # Task flags
        self.sensor_wait_done = False
        self.scan_done        = False
        self.task1_done       = False
        self.task2_done       = False
        self.task5_done       = False

        # Task 1 step flags
        self.t1_survivor_reached = False
        self.t1_waited           = False
        self.t1_tf_published     = False
        self.t1_medkit_reached   = False
        self.t1_returned         = False

        # Task 2 step flags
        self.t2_dam_reached   = False
        self.t2_rotated_left  = False
        self.t2_rotated_right = False

        # Task 5 step flags
        self.t5_exit_reached = False

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Service clients
        self.survivor_tf_client = self.create_client(Trigger, 'publish_survivor_tf')

        # Subscriptions
        self.create_subscription(Bool,    '/fire_safe',              self.fire_safe_cb,      10)
        self.create_subscription(Bool,    '/battery_level_low',      self.battery_cb,        10)
        self.create_subscription(Odometry,'/odom',                   self.odom_cb,           10)
        self.create_subscription(String,  '/detected_colour',        self.detected_colour_cb,10)
        self.create_subscription(Bool,    '/colour_visible',         self.colour_visible_cb, 10)
        self.create_subscription(Float32, '/colour_offset_x',        self.colour_offset_cb,  10)
        self.create_subscription(Float32, '/colour_area',            self.colour_area_cb,    10)
        self.create_subscription(Float32, '/front_obstacle_distance',self.front_dist_cb,     10)
        # Lightweight scan subscriber just to confirm LiDAR bridge is alive
        from sensor_msgs.msg import LaserScan
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)

        self.tree = self._build_tree()
        self.get_logger().info('BTRunner started — waiting for sensors')

    # ─────────────────────────────────────────
    # Callbacks
    # ─────────────────────────────────────────

    def fire_safe_cb(self, msg):
        """
        Receives /fire_safe from fire_safety.py.
        True  = robot is safely away from fire
        False = robot is too close — BT will trigger RetreatFromFire
        """
        self.fire_safe_received = True
        self.fire_too_close = not msg.data

    def battery_cb(self, msg):
        self.battery_low = msg.data

    def detected_colour_cb(self, msg):
        self.detected_colour = msg.data

    def colour_visible_cb(self, msg):
        self.colour_visible = msg.data

    def colour_offset_cb(self, msg):
        self.colour_offset_x = msg.data

    def colour_area_cb(self, msg):
        self.colour_area = msg.data

    def front_dist_cb(self, msg):
        self.front_obstacle_distance = msg.data

    def scan_cb(self, msg):
        self.scan_received = True

    def odom_cb(self, msg):
        self.odom_received = True
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.robot_yaw = math.atan2(siny, cosy)

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────

    def angle_diff(self, a, b):
        d = a - b
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        return d

    # ─────────────────────────────────────────
    # Tree
    # ─────────────────────────────────────────

    def _build_tree(self):

        # ── Wait for all sensor nodes to publish ──
        wait_for_sensors = py_trees.composites.Selector(
            name='SensorReadyWrapper', memory=False,
            children=[
                TaskAlreadyDone('SensorReadySkip', self, 'sensor_wait_done'),
                py_trees.composites.Sequence(
                    name='SensorReadyDo', memory=True,
                    children=[
                        WaitForSensors(self),
                        MarkTaskDone('MarkSensorReady', self, 'sensor_wait_done'),
                    ]
                )
            ]
        )

        # ── Fire safety fallback ──
        fire_safety_fallback = py_trees.composites.Selector(
            name='FireSafetyFallback', memory=False,
            children=[FireSafe(self), RetreatFromFire(self)]
        )

        # ── Battery fallback ──
        charge_with_timeout = py_trees.decorators.Timeout(
            name='ChargeTimeout', child=WaitForCharge(self), duration=60.0
        )

        battery_fallback = py_trees.composites.Selector(
            name='BatteryFallback', memory=False,
            children=[
                BatteryOK(self),
                py_trees.composites.Sequence(
                    name='DockingSequence', memory=True,
                    children=[
                        NavigateToVerified(
                            'GoToDock', self,
                            target_name='dock',
                            expected_colour='black',
                            stop_distance=0.5,
                            verify_timeout=10.0
                        ),
                        charge_with_timeout,
                    ]
                )
            ]
        )

        def step(name, flag_name, action):
            return py_trees.composites.Selector(
                name=f'{name}Wrapper', memory=False,
                children=[
                    TaskAlreadyDone(f'{name}Skip', self, flag_name),
                    py_trees.composites.Sequence(
                        name=f'{name}Do', memory=True,
                        children=[action, MarkTaskDone(f'Mark{name}', self, flag_name)]
                    )
                ]
            )

        # ── Startup scan ──
        startup_scan = py_trees.composites.Selector(
            name='StartupScanWrapper', memory=False,
            children=[
                TaskAlreadyDone('ScanSkip', self, 'scan_done'),
                py_trees.composites.Sequence(
                    name='ScanDo', memory=True,
                    children=[
                        ScanEnvironment(self),
                        MarkTaskDone('MarkScanDone', self, 'scan_done'),
                    ]
                )
            ]
        )

        # ── Task 1: Bring Medical Kit to Survivor ──
        task1_inner = py_trees.composites.Sequence(
            name='Task1_MedicalKit', memory=True,
            children=[
                step('GoToSurvivor', 't1_survivor_reached',
                     NavigateToVerified('GoToSurvivor', self,
                                        target_name='survivor',
                                        expected_colour='green',
                                        stop_distance=1.0)),
                step('WaitOneSec', 't1_waited',
                     WaitSeconds('WaitOneSec', seconds=1.0)),
                step('PublishTF', 't1_tf_published',
                     PublishSurvivorTF(self)),
                step('GoToMedKit', 't1_medkit_reached',
                     NavigateToVerified('GoToMedKit', self,
                                        target_name='medical_kit',
                                        expected_colour='yellow',
                                        stop_distance=0.5)),
                step('ReturnToSurvivor', 't1_returned',
                     NavigateToVerified('ReturnToSurvivor', self,
                                        target_name='survivor',
                                        expected_colour='green',
                                        stop_distance=1.0)),
                MarkTaskDone('MarkTask1Done', self, 'task1_done'),
            ]
        )

        task1 = py_trees.composites.Selector(
            name='Task1Wrapper', memory=False,
            children=[TaskAlreadyDone('Task1Skip', self, 'task1_done'), task1_inner]
        )

        # ── Task 2: Scan Dam ──
        task2_inner = py_trees.composites.Sequence(
            name='Task2_ScanDam', memory=True,
            children=[
                step('GoToDam', 't2_dam_reached',
                     NavigateToVerified('GoToDam', self,
                                        target_name='dam',
                                        expected_colour='blue',
                                        stop_distance=0.5)),
                step('RotateLeft', 't2_rotated_left',
                     RotateRobot('RotateLeft10', self, degrees=10)),
                step('RotateRight', 't2_rotated_right',
                     RotateRobot('RotateRight10', self, degrees=-10)),
                MarkTaskDone('MarkTask2Done', self, 'task2_done'),
            ]
        )

        task2 = py_trees.composites.Selector(
            name='Task2Wrapper', memory=False,
            children=[TaskAlreadyDone('Task2Skip', self, 'task2_done'), task2_inner]
        )

        # ── Task 5: Exit Building ──
        task5_inner = py_trees.composites.Sequence(
            name='Task5_Exit', memory=True,
            children=[
                step('GoToExit', 't5_exit_reached',
                     NavigateToVerified('GoToExit', self,
                                        target_name='exit',
                                        expected_colour='purple',
                                        stop_distance=0.3)),
                MarkTaskDone('MarkTask5Done', self, 'task5_done'),
                StopAndWait(self),
            ]
        )

        task5 = py_trees.composites.Selector(
            name='Task5Wrapper', memory=False,
            children=[TaskAlreadyDone('Task5Skip', self, 'task5_done'), task5_inner]
        )

        # ── Mission root ──
        # Order:
        #   1. WaitForSensors   — block until fire_safety, odom, scan all live
        #   2. FireSafety       — always checked every tick
        #   3. StartupScan      — 360 degree environment scan
        #   4. BatteryFallback  — dock if low
        #   5-7. Tasks
        root = py_trees.composites.Sequence(
            name='Mission', memory=False,
            children=[
                wait_for_sensors,
                fire_safety_fallback,
                startup_scan,
                battery_fallback,
                task1,
                task2,
                task5,
            ]
        )

        return py_trees.trees.BehaviourTree(root)

    def run(self):
        self.tree.setup(timeout=15.0)
        self.get_logger().info('Starting mission BT...')
        while rclpy.ok():
            self.tree.tick()
            rclpy.spin_once(self, timeout_sec=0.1)


def main(args=None):
    rclpy.init(args=args)
    node = BTRunner()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_vel_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()