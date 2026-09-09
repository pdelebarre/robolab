# Architecture

## Robot

Target dimensions are approximately 250 mm overall height. The robot is intentionally stylized: large head, two optical eyes, compact torso, two arms and two feet. The first simulator model prioritizes controllability and behavior validation over photorealism.

## ROS 2 graph

```text
voice_input ───────┐
                    ▼
              behavior_manager
               │     │      │
               ▼     ▼      ▼
          navigation  manipulation  recovery_manager
               │         │             │
               └────┬────┴──────┬──────┘
                    ▼           ▼
               locomotion   perception
                    │           │
                    └─────┬─────┘
                          ▼
                     robot_state
```

### Key interfaces

- `cmd_vel`: desired planar body velocity
- `joint_targets`: desired joint positions
- `camera/left/image_raw`, `camera/right/image_raw`: stereo camera streams
- `imu/data`: body orientation/angular velocity
- `voice/command`: recognized speech command
- `voice/say`: text-to-speech request
- `manipulation/goal`: grasp/carry/drop goal
- `recovery/state`: stand/fallen/recovering/standing

## AI/MCP boundary

OpenCode agents should interact with high-level robot capabilities rather than arbitrary actuator commands. An eventual MCP server should expose commands such as `start_simulation`, `get_robot_state`, `navigate_to`, `find_object`, `pick_object`, `place_object`, `speak`, and `run_behavior_test`.

A future hardware gateway can map the same high-level commands to ROS 2 nodes running on Raspberry Pi and microcontroller firmware on an ESP32. A safety controller remains between high-level commands and physical actuation.
