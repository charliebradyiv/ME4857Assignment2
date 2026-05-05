#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32, Bool
import math


class ObstacleMonitor(Node):
    """
    Subscribes to /scan from the LiDAR and publishes derived information:
      - /min_obstacle_distance   (Float32) closest obstacle anywhere
      - /front_obstacle_distance (Float32) closest obstacle in front arc
      - /left_obstacle_distance  (Float32) closest obstacle on the left
      - /right_obstacle_distance (Float32) closest obstacle on the right
      - /obstacle_in_front       (Bool)    something within emergency_distance ahead

    The side distances are used by the navigator for wall-follow obstacle
    avoidance. ROS REP 103 angle convention: 0 = forward, +ve = left (CCW).
    """
    def __init__(self):
        super().__init__('obstacle_monitor')

        # Parameters — all tunable via launch
        self.declare_parameter('emergency_distance', 0.5)
        self.declare_parameter('front_arc_degrees', 60.0)   # ±30° from forward
        self.declare_parameter('side_arc_min_degrees', 60.0)   # side starts 60° off
        self.declare_parameter('side_arc_max_degrees', 120.0)  # side ends 120° off
        self.emergency_distance = self.get_parameter('emergency_distance').value
        self.front_arc_rad = math.radians(self.get_parameter('front_arc_degrees').value)
        self.side_min_rad = math.radians(self.get_parameter('side_arc_min_degrees').value)
        self.side_max_rad = math.radians(self.get_parameter('side_arc_max_degrees').value)

        # Publishers
        self.min_dist_pub = self.create_publisher(Float32, '/min_obstacle_distance', 10)
        self.front_dist_pub = self.create_publisher(Float32, '/front_obstacle_distance', 10)
        self.left_dist_pub = self.create_publisher(Float32, '/left_obstacle_distance', 10)
        self.right_dist_pub = self.create_publisher(Float32, '/right_obstacle_distance', 10)
        self.front_pub = self.create_publisher(Bool, '/obstacle_in_front', 10)

        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)

        self.get_logger().info('Obstacle Monitor started')

    def scan_cb(self, msg: LaserScan):
        # Filter out invalid readings (0 = no return, very close = noise/self-hit)
        valid_ranges = [r for r in msg.ranges if 0.25 < r < 10.0]

        # Global minimum (any direction)
        if valid_ranges:
            self.min_dist_pub.publish(Float32(data=min(valid_ranges)))
        else:
            self.min_dist_pub.publish(Float32(data=float('inf')))

        # Sweep through each ray. Classify by angle into front / left / right.
        front_min = float('inf')
        left_min = float('inf')
        right_min = float('inf')

        angle = msg.angle_min
        front_half = self.front_arc_rad / 2.0

        for r in msg.ranges:
            if 0.25 < r < 10.0:
                # Front arc: |angle| <= front_half
                if abs(angle) <= front_half:
                    if r < front_min:
                        front_min = r
                # Left arc: side_min <= angle <= side_max  (positive = left)
                elif self.side_min_rad <= angle <= self.side_max_rad:
                    if r < left_min:
                        left_min = r
                # Right arc: -side_max <= angle <= -side_min  (negative = right)
                elif -self.side_max_rad <= angle <= -self.side_min_rad:
                    if r < right_min:
                        right_min = r
            angle += msg.angle_increment

        self.front_dist_pub.publish(Float32(data=front_min))
        self.left_dist_pub.publish(Float32(data=left_min))
        self.right_dist_pub.publish(Float32(data=right_min))

        # Boolean alarm flag
        in_front = front_min < self.emergency_distance
        self.front_pub.publish(Bool(data=in_front))

        if in_front:
            self.get_logger().warn(
                f'Obstacle in front at {front_min:.2f}m',
                throttle_duration_sec=1.0
            )


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()