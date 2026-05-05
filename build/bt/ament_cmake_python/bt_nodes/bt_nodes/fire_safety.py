#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool
import math


class FireSafety(Node):
    """
    Monitors distance to fire and publishes /fire_safe (Bool).
    The BT reads this flag — this node never touches /cmd_vel.
    """
    def __init__(self):
        super().__init__('fire_safety')

        self.fire_x = -14.2
        self.fire_y = 10.8
        self.min_distance = 3.0
        self.robot_x = 0.0
        self.robot_y = 0.0

        self.fire_safe_pub = self.create_publisher(Bool, '/fire_safe', 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.create_timer(0.1, self.check_fire_distance)

        self.get_logger().info('Fire Safety node started')

    def odom_cb(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

    def check_fire_distance(self):
        dist = math.sqrt(
            (self.robot_x - self.fire_x)**2 +
            (self.robot_y - self.fire_y)**2
        )
        msg = Bool()
        msg.data = dist >= self.min_distance
        self.fire_safe_pub.publish(msg)

        if dist < self.min_distance:
            self.get_logger().warn(
                f'Too close to fire! {dist:.2f}m',
                throttle_duration_sec=1.0
            )


def main(args=None):
    rclpy.init(args=args)
    node = FireSafety()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
