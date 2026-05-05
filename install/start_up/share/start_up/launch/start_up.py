#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    robot_model_share = get_package_share_directory('robot_model')
    bt_share = get_package_share_directory('bt')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_model_share, 'launch', 'gazebo.launch.py')
        )
    )

    bt_launch = TimerAction(
        period=25.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(bt_share, 'launch', 'bt_launch.py')
                )
            )
        ]
    )

    return LaunchDescription([
        gazebo_launch,
        bt_launch,
    ])
