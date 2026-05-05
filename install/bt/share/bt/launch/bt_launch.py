from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='bt',
            executable='tf_publisher.py',
            name='tf_publisher',
            output='screen',
        ),
        Node(
            package='bt',
            executable='navigate_to_server.py',
            name='navigate_to_server',
            output='screen',
        ),
        Node(
            package='bt',
            executable='obstacle_monitor.py',
            name='obstacle_monitor',
            output='screen',
        ),
     
        Node(
            package='bt',
            executable='camera_colour_detector.py',
            name='camera_colour_detector',
            output='screen',
        ),
        Node(
            package='bt',
            executable='bt_runner.py',
            name='bt_runner',
            output='screen',
        ),
        Node(
            package='bt',
            executable='battery_monitor.py',
            name='battery_monitor',
            output='screen',
        ),
        Node(
             package='bt',
             executable='fire_safety.py',
              name='fire_safety',
              output='screen',
            ),
        Node(
             package='bt',
             executable='cmd_vel_converter.py',
             name='cmd_vel_converter',
            output='screen',
            ),

])