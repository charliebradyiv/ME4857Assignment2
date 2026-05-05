#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import String, Bool, Float32

from cv_bridge import CvBridge
import cv2
import numpy as np


class CameraColourDetector(Node):
    """
    Detects coloured assignment markers from /camera/image_raw.

    Publishes:
      /detected_colour       std_msgs/String
      /colour_visible        std_msgs/Bool
      /colour_offset_x       std_msgs/Float32
      /colour_area           std_msgs/Float32

    detected_colour values:
      green, blue, yellow, purple, red, black, none
    """

    def __init__(self):
        super().__init__('camera_colour_detector')

        self.bridge = CvBridge()

        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('min_area', 500.0)

        self.image_topic = self.get_parameter('image_topic').value
        self.min_area = float(self.get_parameter('min_area').value)

        self.colour_pub = self.create_publisher(String, '/detected_colour', 10)
        self.visible_pub = self.create_publisher(Bool, '/colour_visible', 10)
        self.offset_pub = self.create_publisher(Float32, '/colour_offset_x', 10)
        self.area_pub = self.create_publisher(Float32, '/colour_area', 10)

        self.create_subscription(Image, self.image_topic, self.image_cb, 10)

        self.get_logger().info(
            f'Camera colour detector started on {self.image_topic}'
        )

    def image_cb(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Image conversion failed: {e}')
            return

        height, width, _ = frame.shape
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        colour_ranges = {
            'green': [
                (np.array([40, 60, 40]), np.array([85, 255, 255]))
            ],
            'blue': [
                (np.array([95, 60, 40]), np.array([130, 255, 255]))
            ],
            'yellow': [
                (np.array([20, 80, 80]), np.array([35, 255, 255]))
            ],
            'purple': [
                (np.array([130, 40, 40]), np.array([165, 255, 255]))
            ],
            'red': [
                (np.array([0, 80, 50]), np.array([10, 255, 255])),
                (np.array([170, 80, 50]), np.array([180, 255, 255]))
            ],
            'black': [
                (np.array([0, 0, 0]), np.array([180, 255, 45]))
            ],
        }

        best_colour = 'none'
        best_area = 0.0
        best_cx = width / 2.0

        kernel = np.ones((5, 5), np.uint8)

        for colour, ranges in colour_ranges.items():
            combined_mask = None

            for lower, upper in ranges:
                mask = cv2.inRange(hsv, lower, upper)
                if combined_mask is None:
                    combined_mask = mask
                else:
                    combined_mask = cv2.bitwise_or(combined_mask, mask)

            combined_mask = cv2.erode(combined_mask, kernel, iterations=1)
            combined_mask = cv2.dilate(combined_mask, kernel, iterations=2)

            contours, _ = cv2.findContours(
                combined_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if not contours:
                continue

            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            if area > best_area:
                moments = cv2.moments(largest)
                if moments['m00'] != 0:
                    best_area = area
                    best_colour = colour
                    best_cx = moments['m10'] / moments['m00']

        visible = best_area >= self.min_area

        colour_msg = String()
        visible_msg = Bool()
        offset_msg = Float32()
        area_msg = Float32()

        colour_msg.data = best_colour if visible else 'none'
        visible_msg.data = visible
        offset_msg.data = float((best_cx - width / 2.0) / (width / 2.0))
        area_msg.data = float(best_area)

        self.colour_pub.publish(colour_msg)
        self.visible_pub.publish(visible_msg)
        self.offset_pub.publish(offset_msg)
        self.area_pub.publish(area_msg)

        if visible:
            self.get_logger().info(
                f'Detected {best_colour}: area={best_area:.1f}, '
                f'offset_x={offset_msg.data:.2f}',
                throttle_duration_sec=1.0
            )


def main(args=None):
    rclpy.init(args=args)
    node = CameraColourDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()