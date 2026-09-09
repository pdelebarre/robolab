# Articulated biped milestone

## Scope

This milestone converts the Webots alien from a static visual model into a
physics-capable articulated lower body with six actuated joints:

- left/right hip
- left/right knee
- left/right ankle

Each joint has a Webots `RotationalMotor` and `PositionSensor`. Both feet are
separate physical solids with bumper contact sensors.

## Control architecture

The `alien_gait` controller uses a deterministic periodic joint-space gait.
The trajectory alternates left/right swing phases and adds bounded IMU pitch
and roll corrections. A fall threshold switches all six motors to a neutral pose.

The gait generator is deliberately pure Python apart from the Webots entry
point. This makes trajectory and safety-state behavior unit-testable without a
Webots installation.

## Validation boundary

The repository now contains a real articulated Webots model and motor/contact
contracts. The unit tests validate deterministic trajectory generation,
balance correction bounds, fall detection and neutralization.

A successful Webots run with stable 1 m locomotion is **not** claimed by this
commit until it is exercised in the simulator. Tuning gait parameters for a
specific dynamics configuration is expected in the next iteration.

## Next

1. Tune gait against measured foot contacts and center-of-mass motion.
2. Add finite-state contact switching for stance/swing timing.
3. Add physics-based push/fall tests and staged get-up poses.
4. Add arm/gripper joints.
5. Bridge sensor state and high-level behavior through ROS 2.
