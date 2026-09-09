# Articulated gait controller

`alien_gait.py` is the first joint-level locomotion controller for the RoboLab 25 cm alien.

## Control model

The controller drives six leg motors:

- hip, knee and ankle on each side
- alternating sinusoidal swing phases
- knee lift during the swing half-cycle
- small pitch/roll IMU corrections
- neutral motor targets when a fall threshold is exceeded

The gait generator is deterministic and has no dependency on Webots, so its
trajectory can be unit-tested independently from simulation.

The Webots entry point is the module's `__main__` block. It expects the world
to expose the six motor names and two foot contact sensors listed below.

## Safety boundary

This is simulation control only. Physical deployment must add an independent
motor safety layer, watchdog, current/thermal limits and hardware emergency stop.
