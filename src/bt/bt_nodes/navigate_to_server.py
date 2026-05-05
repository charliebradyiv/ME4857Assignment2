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

    Architecture (per project brief):
      - Waypoints are predefined (the brief explicitly permits a waypoint
        system: 'A predefined waypoint system' is listed as acceptable).
      - The LiDAR is used for obstacle avoidance via a wall-follow state
        machine that engages when something appears within AVOID_TRIGGER
        metres in front.
      - The IMU's linear_acceleration.x is monitored during forward motion.
        If the robot is commanding forward velocity but the IMU sees no
        measurable acceleration for more than SLIP_TIMEOUT seconds, the
        wheels are inferred to be spinning against an obstacle (wheel slip).
        The robot backs up and rotates to escape before resuming navigation.
        This prevents odometry drift from accumulated encoder counts while
        the robot is physically stuck.

    The action interface is custom (sr_interfaces/NavigateToWaypoint).
    """

    # ── Tunables ─────────────────────────────────────────
    AVOID_TRIGGER        = 0.5   # m  — front distance to enter wall-follow
    AVOID_RESUME_FRONT   = 1.0   # m  — front clearance to exit wall-follow
    WALL_DIST            = 0.5   # m  — target side distance during follow
    AVOID_TIMEOUT        = 30.0  # s  — give up wall-follow, try direct
    LIDAR_CONFIRM_SLOP   = 1.0   # m  — LiDAR confirm slop on top of stop dist
    SLIP_ACCEL_THRESHOLD = 0.08  # m/s² — below this = not accelerating
    SLIP_TIMEOUT         = 3.0   # s  — seconds of no acceleration = stuck

    def __init__(self):
        super().__init__('navigate_to_server')

        # Hardcoded waypoint coordinates (world frame, metres)
        self.waypoints = {
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

        # LiDAR-derived fields
        self.obstacle_in_front       = False
        self.front_obstacle_distance = float('inf')
        self.left_obstacle_distance  = float('inf')
        self.right_obstacle_distance = float('inf')

        # IMU — used to detect wheel slip
        # If forward motion is commanded but IMU shows no acceleration,
        # the wheels are spinning against an obstacle.
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
            self.robot_x = msg.pose.pose.position.x
            self.robot_y = msg.pose.pose.position.y
            q = msg.pose.pose.orientation
            siny = 2.0 * (q.w * q.z + q.x * q.y)
            cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
            self.robot_yaw = math.atan2(siny, cosy)

    def obstacle_cb(self, msg):
        self.obstacle_in_front = msg.data

    def front_dist_cb(self, msg):
        self.front_obstacle_distance = msg.data

    def left_dist_cb(self, msg):
        self.left_obstacle_distance = msg.data

    def right_dist_cb(self, msg):
        self.right_obstacle_distance = msg.data

    def imu_cb(self, msg):
        # Forward acceleration in the robot's body frame.
        # Near zero when stuck; clearly non-zero when actually moving.
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
        self.cmd_vel_pub.publish(Twist())

    def _escape_from_wall(self):
        """Back up then rotate to break free from a wall contact."""
        self.get_logger().warn('Wheel slip confirmed — backing up to escape')
        escape = Twist()
        # Back up
        escape.linear.x = -0.2
        for _ in range(10):
            self.cmd_vel_pub.publish(escape)
            time.sleep(0.1)
        # Rotate away
        escape.linear.x  = 0.0
        escape.angular.z = 0.5
        for _ in range(10):
            self.cmd_vel_pub.publish(escape)
            time.sleep(0.1)
        self.stop()

    # ── Main execute callback ───────────────────────────
    def execute_cb(self, goal_handle):
        with self._nav_lock:
            self._preempt.clear()

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

            # ── State machine ────────────────────────────
            mode             = 'NORMAL'
            follow_side      = None
            avoid_start_time = None

            # IMU wheel-slip timer
            # Tracks when we last had meaningful forward acceleration.
            # Reset whenever we rotate or are in wall-follow mode.
            slip_start = None

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

                # Heading toward goal
                target_angle  = math.atan2(ty - y, tx - x)
                heading_error = self.angle_diff(target_angle, yaw)

                # ── NORMAL mode ──────────────────────────
                if mode == 'NORMAL':

                    # Disable wall-follow when close to goal —
                    # the obstacle in front IS likely the target.
                    near_goal = dist <= 2.0

                    if self.front_obstacle_distance < self.AVOID_TRIGGER and not near_goal:
                        if self.left_obstacle_distance > self.right_obstacle_distance:
                            follow_side = 'right'
                        else:
                            follow_side = 'left'
                        mode             = 'AVOID'
                        avoid_start_time = time.time()
                        slip_start       = None   # reset slip timer — entering avoidance
                        self.get_logger().info(
                            f'Obstacle at {self.front_obstacle_distance:.2f}m — '
                            f'wall-follow on {follow_side} side '
                            f'(L={self.left_obstacle_distance:.2f}m, '
                            f'R={self.right_obstacle_distance:.2f}m)'
                        )
                        time.sleep(0.1)
                        continue

                    # Drive toward goal
                    twist = Twist()
                    if abs(heading_error) > 0.3:
                        # Rotating — reset slip timer, we're not driving forward
                        twist.linear.x  = 0.0
                        twist.angular.z = self.clamp(heading_error * 1.5, -0.8, 0.8)
                        slip_start = None
                    else:
                        twist.linear.x  = min(0.6, dist * 0.5)
                        twist.angular.z = heading_error * 0.5

                        # ── IMU wheel-slip detection ──────────────
                        # Commanding forward motion — check the IMU actually
                        # sees forward acceleration. If not for SLIP_TIMEOUT
                        # seconds, the robot is stuck against something.
                        if self.imu_received:
                            if abs(self.imu_accel_x) < self.SLIP_ACCEL_THRESHOLD:
                                if slip_start is None:
                                    slip_start = time.time()
                                elif time.time() - slip_start > self.SLIP_TIMEOUT:
                                    self.get_logger().warn(
                                        f'Wheel slip detected to {target} '
                                        f'(IMU accel={self.imu_accel_x:.3f} m/s², '
                                        f'odom dist={dist:.2f}m)'
                                    )
                                    self._escape_from_wall()
                                    slip_start = None
                                    continue
                            else:
                                slip_start = None  # moving — reset timer

                    self.cmd_vel_pub.publish(twist)

                # ── AVOID mode ───────────────────────────
                else:
                    # Timeout — give up and try direct path
                    if time.time() - avoid_start_time > self.AVOID_TIMEOUT:
                        self.get_logger().warn(
                            'Wall-follow timeout — returning to direct navigation'
                        )
                        mode        = 'NORMAL'
                        follow_side = None
                        slip_start  = None
                        time.sleep(0.1)
                        continue

                    # Resume direct when front is clear and heading is good
                    front_clear    = self.front_obstacle_distance > self.AVOID_RESUME_FRONT
                    aligned_to_goal = abs(heading_error) < 0.6
                    if front_clear and aligned_to_goal:
                        self.get_logger().info(
                            f'Path clear (front={self.front_obstacle_distance:.2f}m) '
                            f'— resuming direct navigation'
                        )
                        mode        = 'NORMAL'
                        follow_side = None
                        slip_start  = None
                        time.sleep(0.1)
                        continue

                    # Wall-follow: drive forward, steer to maintain WALL_DIST
                    twist = Twist()
                    twist.linear.x = 0.2

                    if follow_side == 'right':
                        error           = self.right_obstacle_distance - self.WALL_DIST
                        twist.angular.z = self.clamp(-error * 1.0, -0.5, 0.5)
                    else:
                        error           = self.left_obstacle_distance - self.WALL_DIST
                        twist.angular.z = self.clamp(error * 1.0, -0.5, 0.5)

                    # Emergency corner rotation
                    if self.front_obstacle_distance < 0.3:
                        twist.linear.x  = 0.0
                        twist.angular.z = 0.6 if follow_side == 'right' else -0.6

                    self.cmd_vel_pub.publish(twist)

                time.sleep(0.1)

            # rclpy shut down
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