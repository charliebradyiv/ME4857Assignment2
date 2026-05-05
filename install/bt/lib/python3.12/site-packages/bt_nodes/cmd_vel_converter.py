#!/usr/bin/env python3
"""
Subscribes to /cmd_vel (geometry_msgs/Twist) and republishes as
/diff_drive_controller/cmd_vel (geometry_msgs/TwistStamped).
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped


class CmdVelConverter(Node):
    def __init__(self):
        super().__init__('cmd_vel_converter')

        self.pub = self.create_publisher(
            TwistStamped,
            '/diff_drive_controller/cmd_vel',
            10
        )

        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cb,
            10
        )

        self.get_logger().info(
            'cmd_vel_converter: /cmd_vel (Twist) -> /diff_drive_controller/cmd_vel (TwistStamped)'
        )

    def cb(self, msg):
        stamped = TwistStamped()
        stamped.header.stamp = self.get_clock().now().to_msg()
        stamped.header.frame_id = 'base_footprint'
        stamped.twist = msg
        self.pub.publish(stamped)


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()