#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class BatteryMonitor(Node):
    def __init__(self):
        super().__init__('battery_monitor')

        self.battery_pub = self.create_publisher(Bool, '/battery_level_low', 10)

        self.battery_level = 100.0
        self.charging = False
        self.battery_low_flag = False

        self.create_timer(1.0, self.update_battery)
        self.get_logger().info('Battery Monitor started')

    def update_battery(self):
        if self.charging:
            self.battery_level = min(100.0, self.battery_level + 2.0)
            if self.battery_level >= 100.0:
                self.charging = False
                self.battery_low_flag = False
                self.get_logger().info('Battery fully charged!')
        else:
            self.battery_level = max(0.0, self.battery_level - 0.5)

        if not self.battery_low_flag and self.battery_level < 20.0:
            self.battery_low_flag = True
            self.charging = True
            self.get_logger().warn(f'Battery low! Level: {self.battery_level:.1f}% — docking to charge')

        msg = Bool()
        msg.data = self.battery_low_flag
        self.battery_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = BatteryMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
