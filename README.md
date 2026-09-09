# RoboLab

AI-assisted robotics laboratory for designing, simulating, and eventually building small robots.

## MVP: cute alien biped

The first target is a 25 cm tall, two-footed alien robot with:

- binocular camera eyes
- microphone input and speaker output
- two arms with simple grippers
- autonomous walking and obstacle avoidance
- visual target selection
- object grasp/carry/drop behavior
- fall detection and recovery behavior
- ROS 2 interfaces suitable for later hardware deployment

The MVP uses **Webots** as the primary simulator and keeps the robot control interfaces transport-neutral so they can later be connected to ESP32/Raspberry Pi hardware.

## Repository layout

```text
robolab/
├── simulation/webots/       # Webots world, robot model and controller
├── ros2/alien_robot/        # ROS 2 Python package
├── mcp/                     # MCP integration design and future server
├── tests/                   # deterministic behavior tests
├── docs/                    # architecture and MVP scope
└── backlog/                 # implementation backlog
```

## MVP scope

This first slice provides a software-first reference implementation. The robot's locomotion, perception, voice, manipulation and recovery interfaces are represented as ROS 2 nodes/classes and can be exercised without physical hardware.

The physical actuator and audio devices are deliberately abstracted behind interfaces. No direct unrestricted motor or power-control path is provided to an LLM.

## Prerequisites

- Ubuntu 24.04 recommended
- ROS 2 Jazzy
- Webots R2025a or newer compatible release
- Python 3.12

## Intended run flow

```bash
# Source ROS 2
source /opt/ros/jazzy/setup.bash

# Build the workspace
cd ros2
colcon build --symlink-install
source install/setup.bash

# Start the robot behavior stack
ros2 launch alien_robot bringup.launch.py simulation:=true
```

Webots integration is kept under `simulation/webots` and can be launched from the ROS 2 stack when the Webots ROS 2 package is installed.

## Safety boundary

Simulation and high-level behaviors may be automated. Physical hardware should add an independent safety layer for speed/current/workspace limits, emergency stop, watchdogs and human approval for hazardous actions.
