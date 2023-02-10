from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition, LaunchConfigurationEquals
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    return LaunchDescription([

        DeclareLaunchArgument(
            name='use_rviz',
            default_value='false',
            choices=['true','false'],
            description='Open RVIZ for Go1 visualization'
        ),

        DeclareLaunchArgument(
            name='fixed_frame',
            default_value='base_footprint',
            description='Fixed frame for RVIZ'
        ),

        DeclareLaunchArgument(
            name='use_lidar',
            default_value='true',
            choices=["true", "false"],
            description='Launch lidar sdk'
        ),

        DeclareLaunchArgument(
            name='use_rtabmap',
            default_value='true',
            choices=["true", "false"],
            description='Launch rtabmap_ros for SLAM'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('unitree_legged_real'),
                    'launch',
                    'high.launch.py'
                ])
            ),
            launch_arguments=[
                ('use_rviz', LaunchConfiguration('use_rviz')),
                ('fixed_frame', LaunchConfiguration('fixed_frame')),
            ],
        ),

        Node(
            package='unitree_nav',
            executable='cmd_processor',
            output='screen'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('rslidar_sdk'),
                    'launch',
                    'start.py'
                ])
            ),
            condition=LaunchConfigurationEquals(
                "use_lidar", "true"
            ),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('rtabmap_ros'),
                    'launch',
                    'rslidar_robosense.launch.py'
                ])
            ),
            condition=LaunchConfigurationEquals(
                "use_rtabmap", "true"
            ),
        ),
    ])