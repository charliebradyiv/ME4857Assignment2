#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Float32
from sensor_msgs.msg import Imu
from sr_interfaces.action import NavigateToWaypoint
import math
import threading
import time


class NavigateToServer(Node):
    """
    Action server that drives the robot to one of a set of HARDCODED waypoint
    coordinates while using the LiDAR for obstacle avoidance and the IMU for
    wheel-slip detection.

    Key design decisions:
      - 'origin' (0,0) is an intermediate waypoint to break long diagonal
        journeys into shorter legs, reducing accumulated odometry drift.
      - During pure rotation (linear.x = 0), the x/y position from /odom
        is FROZEN. The 6-wheel platform causes wheel scrub during in-place
        rotation which the diff_drive_controller misreads as displacement.
        Freezing position during rotation prevents this phantom drift while
        still allowing yaw to update correctly.
      - The IMU's linear_acceleration.x is monitored during forward motion
        to detect wheel slip against walls, triggering a back-up and rotate
        escape manoeuvre.
    """

    # ── Tunables ─────────────────────────────────────────
    AVOID_TRIGGER        = 0.5   # m   — front distance to enter wall-follow
    AVOID_RESUME_FRONT   = 1.0   # m   — front clearance to exit wall-follow
    WALL_DIST            = 0.5   # m   — target side distance during follow
    AVOID_TIMEOUT        = 30.0  # s   — give up wall-follow, try direct
    LIDAR_CONFIRM_SLOP   = 1.0   # m   — LiDAR confirm slop on top of stop dist
    SLIP_ACCEL_THRESHOLD = 0.08  # m/s² — below this = not accelerating
    SLIP_TIMEOUT         = 3.0   # s   — seconds of no acceleration = stuck

    def __init__(self):
        super().__init__('navigate_to_server')

        # Hardcoded waypoint coordinates (world frame, metres).
        # 'origin' is the robot spawn point used as a safe intermediate
        # stop on long diagonal journeys to reduce odometry drift.
        self.waypoints = {
            'origin':      (0.0,    0.0),
            'survivor':    (15.1,  13.4),
            'medical_kit': (-6.3, -16.9),
            'dam':         (8.7,  -11.6),
            'exit':        (2.9,   17.2),
            'dock':        (24.89,  0.0),
        }

        # Pose (updated by /odom)
        self.robot_x   = 0.0
        self.robot_y   = 0.0
        self.robot_yaw = 0.0
        self._lock = threading.Lock()

        # Rotation freeze flag.
        # When True, odom_cb does NOT update x/y — only yaw is updated.
        # This prevents wheel-scrub phantom displacement during pure rotation.
        self._rotating = False

        # LiDAR-derived fields
        self.obstacle_in_front       = False
        self.front_obstacle_distance = float('inf')
        self.left_obstacle_distance  = float('inf')
        self.right_obstacle_distance = float('inf')

        # IMU — used to detect wheel slip
        self.imu_accel_x  = 0.0
        self.imu_received = False

        # Preemption
        self._preempt  = threading.Event()
        self._nav_lock = threading.Lock()

        cb_group = ReentrantCallbackGroup()

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_subscription(Odometry, '/odom',
                                 self.odom_cb, 10, callback_group=cb_group)
        self.create_subscription(Bool, '/obstacle_in_front',
                                 self.obstacle_cb, 10, callback_group=cb_group)
        self.create_subscription(Float32, '/front_obstacle_distance',
                                 self.front_dist_cb, 10, callback_group=cb_group)
        self.create_subscription(Float32, '/left_obstacle_distance',
                                 self.left_dist_cb, 10, callback_group=cb_group)
        self.create_subscription(Float32, '/right_obstacle_distance',
                                 self.right_dist_cb, 10, callback_group=cb_group)
        self.create_subscription(Imu, '/imu',
                                 self.imu_cb, 10, callback_group=cb_group)

        self._action_server = ActionServer(
            self, NavigateToWaypoint, 'navigate_to_waypoint',
            self.execute_cb,
            goal_callback=self._handle_goal,
            cancel_callback=self._handle_cancel,
            callback_group=cb_group
        )
        self.get_logger().info('NavigateToServer ready')

    # ── Goal lifecycle ──────────────────────────────────
    def _handle_goal(self, goal_request):
        if self._nav_lock.locked():
            self._preempt.set()
        return GoalResponse.ACCEPT

    def _handle_cancel(self, goal_handle):
        return CancelResponse.ACCEPT

    # ── Subscriber callbacks ────────────────────────────
    def odom_cb(self, msg):
        with self._lock:
            # Always update yaw — rotation is real and correct.
            q = msg.pose.pose.orientation
            siny = 2.0 * (q.w * q.z + q.x * q.y)
            cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
            self.robot_yaw = math.atan2(siny, cosy)

            # Only update x/y when NOT doing a pure rotation.
            # During pure rotation the 6-wheel geometry causes wheel scrub
            # which the diff_drive_controller misreads as displacement.
            # Freezing x/y during rotation prevents phantom drift.
            if not self._rotating:
                self.robot_x = msg.pose.pose.position.x
                self.robot_y = msg.pose.pose.position.y

    def obstacle_cb(self, msg):
        self.obstacle_in_front = msg.data

    def front_dist_cb(self, msg):
        self.front_obstacle_distance = msg.data

    def left_dist_cb(self, msg):
        self.left_obstacle_distance = msg.data

    def right_dist_cb(self, msg):
        self.right_obstacle_distance = msg.data

    def imu_cb(self, msg):
        self.imu_accel_x  = msg.linear_acceleration.x
        self.imu_received = True

    # ── Helpers ─────────────────────────────────────────
    def get_pose(self):
        with self._lock:
            return self.robot_x, self.robot_y, self.robot_yaw

    @staticmethod
    def angle_diff(a, b):
        d = a - b
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        return d

    @staticmethod
    def clamp(value, lo, hi):
        return max(lo, min(hi, value))

    def stop(self):
        self._rotating = False
        self.cmd_vel_pub.publish(Twist())

    def _escape_from_wall(self):
        """Back up then rotate to break free from a wall contact."""
        self.get_logger().warn('Wheel slip confirmed — backing up to escape')
        escape = Twist()
        # Back up — position updates are valid during reverse
        self._rotating = False
        escape.linear.x = -0.2
        for _ in range(10):
            self.cmd_vel_pub.publish(escape)
            time.sleep(0.1)
        # Rotate to face away — freeze position during this rotation
        self._rotating = True
        escape.linear.x  = 0.0
        escape.angular.z = 0.5
        for _ in range(10):
            self.cmd_vel_pub.publish(escape)
            time.sleep(0.1)
        self._rotating = False
        self.stop()

    # ── Main execute callback ───────────────────────────
    def execute_cb(self, goal_handle):
        with self._nav_lock:
            self._preempt.clear()
            self._rotating = False

            target        = goal_handle.request.target_name
            stop_distance = goal_handle.request.stop_distance

            self.get_logger().info(
                f'Navigating to {target} (odom stop at {stop_distance:.2f}m, '
                f'LiDAR for avoidance)'
            )

            if target not in self.waypoints:
                goal_handle.abort()
                result = NavigateToWaypoint.Result()
                result.success = False
                result.message = f'Unknown waypoint: {target}'
                return result

            tx, ty = self.waypoints[target]
            feedback = NavigateToWaypoint.Feedback()

            mode             = 'NORMAL'
            follow_side      = None
            avoid_start_time = None
            slip_start       = None

            while rclpy.ok():

                # ── Preemption ───────────────────────────
                if self._preempt.is_set():
                    self.stop()
                    goal_handle.abort()
                    result = NavigateToWaypoint.Result()
                    result.success = False
                    result.message = 'Preempted by new goal'
                    return result

                x, y, yaw = self.get_pose()
                dist = math.sqrt((x - tx) ** 2 + (y - ty) ** 2)

                feedback.distance_remaining = dist
                goal_handle.publish_feedback(feedback)

                # ── Arrival check ────────────────────────
                if dist <= stop_distance:
                    self.stop()
                    front = self.front_obstacle_distance
                    if front <= stop_distance + self.LIDAR_CONFIRM_SLOP:
                        self.get_logger().info(
                            f'Reached {target} '
                            f'(odom={dist:.2f}m, LiDAR={front:.2f}m — confirmed)'
                        )
                    else:
                        self.get_logger().warn(
                            f'Reached {target} by odometry '
                            f'(odom={dist:.2f}m, LiDAR={front:.2f}m — '
                            f'no nearby return; target may be small/thin)'
                        )
                    goal_handle.succeed()
                    result = NavigateToWaypoint.Result()
                    result.success = True
                    result.message = f'Reached {target}'
                    return result

                target_angle  = math.atan2(ty - y, tx - x)
                heading_error = self.angle_diff(target_angle, yaw)

                # ── NORMAL mode ──────────────────────────
                if mode == 'NORMAL':

                    near_goal = dist <= 2.0

                    if (self.front_obstacle_distance < self.AVOID_TRIGGER
                            and not near_goal):
                        if self.left_obstacle_distance > self.right_obstacle_distance:
                            follow_side = 'right'
                        else:
                            follow_side = 'left'
                        mode             = 'AVOID'
                        avoid_start_time = time.time()
                        slip_start       = None
                        self._rotating   = False
                        self.get_logger().info(
                            f'Obstacle at {self.front_obstacle_distance:.2f}m — '
                            f'wall-follow on {follow_side} side '
                            f'(L={self.left_obstacle_distance:.2f}m, '
                            f'R={self.right_obstacle_distance:.2f}m)'
                        )
                        time.sleep(0.1)
                        continue

                    twist = Twist()
                    if abs(heading_error) > 0.3:
                        # Pure rotation — freeze x/y to prevent scrub drift
                        self._rotating  = True
                        twist.linear.x  = 0.0
                        twist.angular.z = self.clamp(heading_error * 1.5, -0.8, 0.8)
                        slip_start = None
                    else:
                        # Driving forward — position updates valid
                        self._rotating  = False
                        twist.linear.x  = min(1.0, dist * 0.5)
                        twist.angular.z = heading_error * 0.5

                        # ── IMU wheel-slip detection ──────────────────────
                        if self.imu_received:
                            if abs(self.imu_accel_x) < self.SLIP_ACCEL_THRESHOLD:
                                if slip_start is None:
                                    slip_start = time.time()
                                elif time.time() - slip_start > self.SLIP_TIMEOUT:
                                    self.get_logger().warn(
                                        f'Wheel slip detected navigating to {target} '
                                        f'(IMU accel={self.imu_accel_x:.3f} m/s², '
                                        f'odom dist={dist:.2f}m)'
                                    )
                                    self._escape_from_wall()
                                    slip_start = None
                                    continue
                            else:
                                slip_start = None

                    self.cmd_vel_pub.publish(twist)

                # ── AVOID mode ───────────────────────────
                else:
                    if time.time() - avoid_start_time > self.AVOID_TIMEOUT:
                        self.get_logger().warn(
                            'Wall-follow timeout — returning to direct navigation'
                        )
                        self._rotating = False
                        mode           = 'NORMAL'
                        follow_side    = None
                        slip_start     = None
                        time.sleep(0.1)
                        continue

                    front_clear     = (self.front_obstacle_distance >
                                       self.AVOID_RESUME_FRONT)
                    aligned_to_goal = abs(heading_error) < 0.6
                    if front_clear and aligned_to_goal:
                        self.get_logger().info(
                            f'Path clear (front={self.front_obstacle_distance:.2f}m)'
                            f' — resuming direct navigation'
                        )
                        self._rotating = False
                        mode           = 'NORMAL'
                        follow_side    = None
                        slip_start     = None
                        time.sleep(0.1)
                        continue

                    # Wall-follow: position updates valid (moving forward)
                    self._rotating = False
                    twist = Twist()
                    twist.linear.x = 0.3

                    if follow_side == 'right':
                        error           = self.right_obstacle_distance - self.WALL_DIST
                        twist.angular.z = self.clamp(-error * 1.0, -0.5, 0.5)
                    else:
                        error           = self.left_obstacle_distance - self.WALL_DIST
                        twist.angular.z = self.clamp(error * 1.0, -0.5, 0.5)

                    if self.front_obstacle_distance < 0.3:
                        # Sharp corner turn — freeze position
                        self._rotating  = True
                        twist.linear.x  = 0.0
                        twist.angular.z = 0.6 if follow_side == 'right' else -0.6

                    self.cmd_vel_pub.publish(twist)

                time.sleep(0.1)

            self.stop()
            goal_handle.abort()
            result = NavigateToWaypoint.Result()
            result.success = False
            result.message = 'Navigation aborted'
            return result


def main(args=None):
    rclpy.init(args=args)
    node = NavigateToServer()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()