#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from std_srvs.srv import Trigger
import tf2_ros


class TFPublisher(Node):
    """
    Publishes static world-frame TFs:
      1. map -> odom identity transform (anchors the moving odom frame
         to the fixed world frame at the spawn location)
      2. map -> survivor when triggered by the BT after the survivor
         is reached (Task 1 step 4)

    NOTE: the odom -> base_footprint transform is published by the
    diff_drive_controller (enable_odom_tf: true in the YAML), so this
    node does NOT publish it.
    """

    def __init__(self):
        super().__init__('tf_publisher')

        # Static broadcaster — used for both map->odom and map->survivor
        self.static_broadcaster = tf2_ros.StaticTransformBroadcaster(self)

        # Survivor location from the assignment world
        self.survivor_x = 15.1
        self.survivor_y = 13.4
        self.survivor_tf_published = False

        # 1) Publish the map -> odom anchor immediately at startup.
        #    Robot spawns at (0,0) so map and odom are coincident.
        self.publish_map_to_odom()

        # 2) Service that the BT calls once to publish the survivor TF
        self.create_service(
            Trigger,
            'publish_survivor_tf',
            self.publish_survivor_tf_cb
        )

        self.get_logger().info('TF Publisher node started')

    def publish_map_to_odom(self):
        """Anchor the moving odom frame to the fixed map frame at startup."""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'odom'
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.w = 1.0  # identity rotation
        self.static_broadcaster.sendTransform(t)
        self.get_logger().info('Published static map -> odom transform')

    def publish_survivor_tf_cb(self, request, response):
        """Service called by the BT after Task 1's wait — publishes survivor TF once."""
        if not self.survivor_tf_published:
            self.publish_survivor_tf()
        response.success = True
        response.message = 'Survivor TF published'
        return response

    def publish_survivor_tf(self):
        self.get_logger().info('Publishing survivor TF relative to spawn (map frame)')

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'           # ← was 'odom'; now 'map'
        t.child_frame_id = 'survivor'
        t.transform.translation.x = self.survivor_x
        t.transform.translation.y = self.survivor_y
        t.transform.translation.z = 0.0
        t.transform.rotation.w = 1.0
        self.static_broadcaster.sendTransform(t)

        self.survivor_tf_published = True
        self.get_logger().info(
            f'Survivor TF published at map=({self.survivor_x}, {self.survivor_y})'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TFPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()