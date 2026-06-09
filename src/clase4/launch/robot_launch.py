import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():

    default_robot = 'mycobot_320_m5_2022/mycobot_320_m5_2022.urdf'

    robot_arg = DeclareLaunchArgument(
        'robot',
        default_value=default_robot,
        description='URDF relativo dentro de robot_description/'
    )

    urdf_file = PathJoinSubstitution([
        FindPackageShare('clase4'),
        'robot_description',
        LaunchConfiguration('robot')
    ])

    robot_description = ParameterValue(
        Command(['cat', ' ', urdf_file]),
        value_type=str
    )
    return LaunchDescription([
        robot_arg,

        LogInfo(msg=['URDF: ', urdf_file]),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d',
                os.path.join(
                    get_package_share_directory('clase4'),
                    'config',
                    'display.rviz'
                )
            ]
        )
    ])