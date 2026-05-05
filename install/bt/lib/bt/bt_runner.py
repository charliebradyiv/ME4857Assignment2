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

class BatteryOK(py_trees.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__('BatteryOK')
        self.node = node

    def update(self):
        if self.node.battery_low:
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.SUCCESS


class FireSafe(py_trees.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__('FireSafe')
        self.node = node

    def update(self):
        if self.node.fire_too_close:
            self.node.get_logger().warn('Fire safety: too close to fire!')
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.SUCCESS


class RetreatFromFire(py_trees.behaviour.Behaviour):
    BUFFER = 0.5

    def __init__(self, node):
        super().__init__('RetreatFromFire')
        self.node = node

    def update(self):
        dx = self.node.robot_x - self.node.fire_x
        dy = self.node.robot_y - self.node.fire_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist >= self.node.fire_min_dist + self.BUFFER:
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
            f'Retreating from fire — {dist:.2f}m of {self.node.fire_min_dist}m',
            throttle_duration_sec=1.0
        )
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        self.node.cmd_vel_pub.publish(Twist())


class ScanEnvironment(py_trees.behaviour.Behaviour):
    """
    Rotates 360 degrees at startup and records the best bearing for each colour.
    Scan progress is stored on the node so battery/fire interruptions don't reset it.
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
                    f'offset={self.node.colour_offset_x:.2f}  '
                    f'bearing={math.degrees(bearing):.1f} deg  '
                    f'area={area:.0f}'
                )

        if self.node._scan_rotated >= self.FULL_ROTATION:
            self.node.cmd_vel_pub.publish(Twist())
            del self.node._scan_rotated
            del self.node._scan_best_areas
            self.node.get_logger().info(
                f'Scan complete. Bearings: {list(self.node.colour_bearings.keys())}'
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


class NavigateToColour(py_trees.behaviour.Behaviour):
    """
    Drives the robot to a target colour using camera + LiDAR.

    Phases:
      TURN_TO_BEARING — rotate to the bearing recorded during the startup scan
      SEARCH          — rotate slowly until target colour is visible
      DRIVE           — drive forward with steering correction

    Key design: once in DRIVE, the robot keeps moving forward even if the
    colour temporarily disappears (up to LOST_THRESHOLD ticks). It only
    falls back to SEARCH if the colour is consistently absent. This prevents
    oscillation when two objects are near each other.
    """

    BEARING_THRESHOLD = 0.2   # rad (~11 deg) — close enough to recorded bearing
    LOST_THRESHOLD    = 8     # consecutive ticks without colour before re-searching

    def __init__(self, name, node, target_colour, stop_distance=1.0, timeout=120.0):
        super().__init__(name)
        self.node         = node
        self.target_colour = target_colour
        self.stop_distance = stop_distance
        self.timeout       = timeout
        self._start        = None
        self._phase        = 'SEARCH'
        self._lost_count   = 0

    def initialise(self):
        self._start      = time.time()
        self._lost_count = 0

        if self.target_colour in self.node.colour_bearings:
            self._phase = 'TURN_TO_BEARING'
            self.node.get_logger().info(
                f'NavigateToColour [{self.target_colour}]: turning to scan bearing '
                f'{math.degrees(self.node.colour_bearings[self.target_colour]):.1f} deg'
            )
        else:
            self._phase = 'SEARCH'
            self.node.get_logger().info(
                f'NavigateToColour [{self.target_colour}]: no bearing — rotating to search'
            )

    def update(self):
        if time.time() - self._start > self.timeout:
            self.node.cmd_vel_pub.publish(Twist())
            self.node.get_logger().warn(
                f'NavigateToColour [{self.target_colour}]: timeout'
            )
            return py_trees.common.Status.FAILURE

        on_target = (
            self.node.colour_visible and
            self.node.detected_colour == self.target_colour
        )

        # ── Stop condition ──────────────────────────────────────────────────
        if on_target and self.node.front_obstacle_distance <= self.stop_distance:
            self.node.cmd_vel_pub.publish(Twist())
            self.node.get_logger().info(
                f'Reached {self.target_colour}: '
                f'LiDAR={self.node.front_obstacle_distance:.2f}m'
            )
            return py_trees.common.Status.SUCCESS

        twist = Twist()

        # ── Phase: TURN_TO_BEARING ──────────────────────────────────────────
        if self._phase == 'TURN_TO_BEARING':
            bearing = self.node.colour_bearings.get(self.target_colour)
            if bearing is None:
                self._phase = 'SEARCH'
            else:
                heading_error = self.node.angle_diff(bearing, self.node.robot_yaw)
                if abs(heading_error) < self.BEARING_THRESHOLD:
                    # Arrived at bearing — go straight to DRIVE if colour visible,
                    # otherwise SEARCH
                    self._phase = 'DRIVE' if on_target else 'SEARCH'
                    self.node.get_logger().info(
                        f'[{self.target_colour}] bearing reached → {self._phase}'
                    )
                else:
                    twist.angular.z = max(-0.6, min(0.6, heading_error * 1.5))
                    self.node.get_logger().info(
                        f'Turning to bearing for {self.target_colour}: '
                        f'error={math.degrees(heading_error):.1f} deg',
                        throttle_duration_sec=1.0
                    )

        # ── Phase: SEARCH ───────────────────────────────────────────────────
        if self._phase == 'SEARCH':
            if on_target:
                self._phase      = 'DRIVE'
                self._lost_count = 0
                self.node.get_logger().info(
                    f'[{self.target_colour}] found — switching to DRIVE'
                )
            else:
                twist.angular.z = 0.3
                self.node.get_logger().info(
                    f'Searching for {self.target_colour} — '
                    f'sees: {self.node.detected_colour}',
                    throttle_duration_sec=1.0
                )

        # ── Phase: DRIVE ────────────────────────────────────────────────────
        if self._phase == 'DRIVE':
            if on_target:
                # Colour visible — drive forward and steer toward it
                self._lost_count = 0
                dist  = self.node.front_obstacle_distance
                # Scale speed: fast when far, slow as we approach
                speed = min(0.8, max(0.15, (dist - self.stop_distance) * 0.8))
                twist.linear.x  = speed
                # Stronger steering correction to track the colour
                twist.angular.z = -0.8 * self.node.colour_offset_x
                self.node.get_logger().info(
                    f'Driving to {self.target_colour}: '
                    f'offset={self.node.colour_offset_x:.2f} '
                    f'LiDAR={dist:.2f}m speed={speed:.2f}',
                    throttle_duration_sec=1.0
                )
            else:
                # Colour temporarily lost — keep moving slowly and rotating to recover
                self._lost_count += 1
                if self._lost_count > self.LOST_THRESHOLD:
                    # Lost for too long — full search rotation
                    self._phase      = 'SEARCH'
                    self._lost_count = 0
                    twist.angular.z  = 0.3
                    self.node.get_logger().info(
                        f'[{self.target_colour}] lost for {self.LOST_THRESHOLD} '
                        f'ticks — returning to SEARCH'
                    )
                else:
                    # Briefly lost — creep forward and rotate slightly to recover
                    twist.linear.x  = 0.1
                    twist.angular.z = 0.2
                    self.node.get_logger().info(
                        f'[{self.target_colour}] briefly lost '
                        f'({self._lost_count}/{self.LOST_THRESHOLD}) — recovering',
                        throttle_duration_sec=1.0
                    )

        self.node.cmd_vel_pub.publish(twist)
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        self.node.cmd_vel_pub.publish(Twist())


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


class GoToDock(py_trees.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__('GoToDock')
        self.node = node
        self._client = ActionClient(node, NavigateToWaypoint, 'navigate_to_waypoint')
        self._goal_handle = None
        self._result = None
        self._sent = False

    def initialise(self):
        self._sent = False
        self._goal_handle = None
        self._result = None

    def update(self):
        if not self._sent:
            if not self._client.wait_for_server(timeout_sec=2.0):
                self.node.get_logger().error('Action server not available for dock')
                return py_trees.common.Status.FAILURE
            goal = NavigateToWaypoint.Goal()
            goal.target_name  = 'dock'
            goal.stop_distance = 0.5
            self._future = self._client.send_goal_async(goal)
            self._sent = True
            self._future.add_done_callback(self._goal_response_cb)
            return py_trees.common.Status.RUNNING

        rclpy.spin_once(self.node, timeout_sec=0.0)

        if self._result is None:
            return py_trees.common.Status.RUNNING
        if self._result.success:
            self.node.get_logger().info('Reached dock')
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE

    def _goal_response_cb(self, future):
        self._goal_handle = future.result()
        if self._goal_handle.accepted:
            result_future = self._goal_handle.get_result_async()
            result_future.add_done_callback(self._result_cb)
        else:
            self.node.get_logger().error('Dock goal rejected')

    def _result_cb(self, future):
        self._result = future.result().result

    def terminate(self, new_status):
        if self._goal_handle is not None:
            self._goal_handle.cancel_goal_async()


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

        # Robot state
        self.battery_low    = False
        self.fire_too_close = False
        self.robot_x        = 0.0
        self.robot_y        = 0.0
        self.robot_yaw      = 0.0

        # Fire position
        self.fire_x        = -14.2
        self.fire_y        = 10.8
        self.fire_min_dist = 3.0

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
        self.scan_done  = False
        self.task1_done = False
        self.task2_done = False
        self.task5_done = False

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
        self.create_subscription(Bool,     '/battery_level_low',       self.battery_cb,        10)
        self.create_subscription(Odometry, '/odom',                    self.odom_cb,            10)
        self.create_subscription(String,   '/detected_colour',         self.detected_colour_cb, 10)
        self.create_subscription(Bool,     '/colour_visible',          self.colour_visible_cb,  10)
        self.create_subscription(Float32,  '/colour_offset_x',         self.colour_offset_cb,   10)
        self.create_subscription(Float32,  '/colour_area',             self.colour_area_cb,     10)
        self.create_subscription(Float32,  '/front_obstacle_distance', self.front_dist_cb,      10)

        self.tree = self._build_tree()
        self.get_logger().info('BTRunner started')

    # ─────────────────────────────────────────
    # Callbacks
    # ─────────────────────────────────────────

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

    def odom_cb(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.robot_yaw = math.atan2(siny, cosy)
        dist = math.sqrt(
            (self.robot_x - self.fire_x) ** 2 +
            (self.robot_y - self.fire_y) ** 2
        )
        self.fire_too_close = dist < self.fire_min_dist

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

        fire_safety_fallback = py_trees.composites.Selector(
            name='FireSafetyFallback', memory=False,
            children=[FireSafe(self), RetreatFromFire(self)]
        )

        charge_with_timeout = py_trees.decorators.Timeout(
            name='ChargeTimeout', child=WaitForCharge(self), duration=60.0
        )

        battery_fallback = py_trees.composites.Selector(
            name='BatteryFallback', memory=False,
            children=[
                BatteryOK(self),
                py_trees.composites.Sequence(
                    name='DockingSequence', memory=True,
                    children=[GoToDock(self), charge_with_timeout]
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

        # Startup scan
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

        # Task 1: Bring Medical Kit to Survivor
        task1_inner = py_trees.composites.Sequence(
            name='Task1_MedicalKit', memory=True,
            children=[
                step('GoToSurvivor',    't1_survivor_reached',
                     NavigateToColour('GoToSurvivor', self, 'green', stop_distance=1.0)),
                step('WaitOneSec',      't1_waited',
                     WaitSeconds('WaitOneSec', seconds=1.0)),
                step('PublishTF',       't1_tf_published',
                     PublishSurvivorTF(self)),
                step('GoToMedKit',      't1_medkit_reached',
                     NavigateToColour('GoToMedKit', self, 'yellow', stop_distance=0.5)),
                step('ReturnToSurvivor','t1_returned',
                     NavigateToColour('ReturnToSurvivor', self, 'green', stop_distance=1.0)),
                MarkTaskDone('MarkTask1Done', self, 'task1_done'),
            ]
        )

        task1 = py_trees.composites.Selector(
            name='Task1Wrapper', memory=False,
            children=[TaskAlreadyDone('Task1Skip', self, 'task1_done'), task1_inner]
        )

        # Task 2: Scan Dam
        task2_inner = py_trees.composites.Sequence(
            name='Task2_ScanDam', memory=True,
            children=[
                step('GoToDam',     't2_dam_reached',
                     NavigateToColour('GoToDam', self, 'blue', stop_distance=0.5)),
                step('RotateLeft',  't2_rotated_left',
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

        # Task 5: Exit Building
        task5_inner = py_trees.composites.Sequence(
            name='Task5_Exit', memory=True,
            children=[
                step('GoToExit', 't5_exit_reached',
                     NavigateToColour('GoToExit', self, 'purple', stop_distance=0.3)),
                MarkTaskDone('MarkTask5Done', self, 'task5_done'),
                StopAndWait(self),
            ]
        )

        task5 = py_trees.composites.Selector(
            name='Task5Wrapper', memory=False,
            children=[TaskAlreadyDone('Task5Skip', self, 'task5_done'), task5_inner]
        )

        root = py_trees.composites.Sequence(
            name='Mission', memory=False,
            children=[
                fire_safety_fallback,
                battery_fallback,
                startup_scan,
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