import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('robot_model')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
    gazebo_worlds_share = get_package_share_directory('gazebo_worlds')

    urdf_file = os.path.join(pkg_share, 'urdf', 'robot_model.urdf')
    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    # Path to the assignment world SDF
    world_file = os.path.join(gazebo_worlds_share, 'worlds', 'assignment_world.sdf')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    install_share_root = os.path.dirname(pkg_share)

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock'
        ),

        # Make Gazebo aware of the installed package share so it can resolve
        # package:// URIs in the URDF meshes
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=install_share_root
        ),

        # Launch Gazebo Harmonic with the assignment world
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
            ),
            launch_arguments={'gz_args': f'-r {world_file}'}.items(),
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': use_sim_time,
            }]
        ),

        # Spawn robot into Gazebo Harmonic via ros_gz_sim
        Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_robot',
            output='screen',
            arguments=[
                '-name', 'robot_model',
                '-topic', 'robot_description',
                '-x', '0.0',
                '-y', '0.0',
                '-z', '0.1',
            ]
        ),

        # Bridge ROS2 <-> Gazebo for clock, joint states, and cmd_vel
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='gz_bridge',
            output='screen',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/model/robot_model/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
            ]
        ),
    ])
