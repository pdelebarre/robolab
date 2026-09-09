# RoboAlien Webots simulation

The current MVP world is `worlds/alien_mvp.wbt` and uses the `RoboAlienMVP` primitive robot in `protos/`.

## Demo controls

Run the world with Webots and use the keyboard:

- `G` — walk to the toy, grasp it, and return home
- `W` — walk home
- `F` — simulate a fall and recover
- `R` — continue recovery
- `H` — reset to standing/home

The controller also enables both camera eyes, IMU, gyro, accelerometer, range sensor, microphone and speaker devices. Voice recognition is intentionally represented by the ROS 2 `voice/command` interface in this slice; an STT adapter will be added next.

## Important MVP boundary

The current walking and recovery motion is a deterministic Supervisor demonstration. It is **not** yet a physically validated biped gait or whole-body controller. The next slice replaces scripted body motion with joint-level motors, balance feedback and contact-aware recovery.
