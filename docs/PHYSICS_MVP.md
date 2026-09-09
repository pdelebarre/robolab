# Physics MVP

## Goal

Move RoboLab from a scripted behavior demonstration toward a physics-based 25 cm biped simulation.

## Current slice

The Webots world establishes the robot scale, alien geometry, two camera eyes, inertial sensors, front range sensor, microphone and speaker, plus an obstacle and graspable toy. A controller exercises the sensor/audio interfaces.

## Next engineering slice

1. Replace primitive torso/leg geometry with articulated `HingeJoint`/`Solid` chains.
2. Add hip, knee and ankle motors with position/velocity limits.
3. Add foot collision/contact sensors.
4. Implement a deterministic periodic gait generator.
5. Add IMU-based pitch/roll stabilization.
6. Add push/fall scenario and contact-aware recovery poses.
7. Add arm joints and gripper actuator.
8. Bridge camera frames and range data into ROS 2.
9. Add speech-to-text and text-to-speech adapters.

## Acceptance scenarios

- Walk 1 m without falling in the nominal world.
- Avoid the obstacle and reach the toy.
- Grasp and carry the toy to the home zone.
- Recover from controlled forward/backward pushes.
- Recover from a full fall using a staged get-up motion.
- Camera topics remain available during locomotion.
- Voice command reaches the behavior manager.

## Safety

Simulation can be automated. Physical deployment must retain an independent safety controller, watchdog and emergency stop; high-level AI commands must never bypass those controls.
