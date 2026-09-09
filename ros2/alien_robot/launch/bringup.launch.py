#!/usr/bin/env python3
from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    simulation = LaunchConfiguration("simulation")
    return LaunchDescription([
        DeclareLaunchArgument("simulation", default_value="true"),
        Node(
            package="alien_robot",
            executable="behavior_manager",
            name="behavior_manager",
            output="screen",
        ),
    ])
