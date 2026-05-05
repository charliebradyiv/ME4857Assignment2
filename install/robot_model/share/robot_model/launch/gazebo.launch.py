#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    TimerAction, ExecuteProcess, DeclareLaunchArgument, RegisterEventHandler,
)
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('robot_model')
    gazebo_worlds_share = get_package_share_directory('gazebo_worlds')
    world_file = os.path.join(gazebo_worlds_share, 'worlds', 'assignment_world.sdf')

    print(f'\n>>> WORLD FILE: {world_file}')
    print(f'>>> EXISTS: {os.path.exists(world_file)}\n')

    urdf_path = os.path.join(pkg_share, 'urdf', 'robot_model.urdf')
    with open(urdf_path, 'r') as f:
        urdf_content = f.read()
    urdf_content = urdf_content.replace('$(find robot_model)', pkg_share)
    robot_description = {'robot_description': urdf_content}

    Start_gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-v', '4', world_file],
        output='screen',
        additional_env={
            'GZ_SIM_SYSTEM_PLUGIN_PATH': '/opt/ros/jazzy/lib',
            'GZ_SIM_RESOURCE_PATH': os.path.dirname(pkg_share),
        },
    )

    Start_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}],
    )

    Spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'robot_model',
            '-x', '0.0', '-y', '0.0', '-z', '0.2',
        ],
    )

    Spawn_jsb = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '30',
        ],
        output='screen',
    )

    Spawn_diff_drive = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '30',
        ],
        output='screen',
    )

    load_jsb_after_robot = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=Spawn_robot,
            on_exit=[Spawn_jsb],
        )
    )
    load_diff_after_jsb = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=Spawn_jsb,
            on_exit=[
                TimerAction(period=3.0, actions=[Spawn_diff_drive]),
            ],
        )
    )

    Cmd_vel_converter = Node(
        package='bt',
        executable='cmd_vel_converter.py',
        name='cmd_vel_converter',
        output='screen',
    )

    Odom_relay = Node(
        package='topic_tools',
        executable='relay',
        name='odom_relay',
        arguments=['/diff_drive_controller/odom', '/odom'],
        output='screen',
    )

    Start_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='gz_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/image_raw/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
        ],
    )

    Start_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz')),
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true', description='Open RViz'),
        Start_gazebo,
        Start_robot_state_publisher,
        TimerAction(period=3.0, actions=[Spawn_robot]),
        TimerAction(period=4.0, actions=[Start_bridge]),
        load_jsb_after_robot,
        load_diff_after_jsb,
        Cmd_vel_converter,
        Odom_relay,
        TimerAction(period=2.0, actions=[Start_rviz]),
    ])