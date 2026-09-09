# RoboAlien Webots simulation

The Webots launcher is designed to work on macOS and Linux without relying on the operating system's `.wbt` file association.

## Start the simulation

From the repository root:

```bash
npm run simulation
```

Or directly:

```bash
bash simulation/webots/run.sh
```

The launcher:

1. Uses `webots` from `PATH` when available.
2. Falls back to the standard macOS installation at `/Applications/Webots.app/Contents/MacOS/webots`.
3. Supports an explicit executable with `WEBOTS_BIN=/path/to/webots`.
4. Opens `worlds/alien_biped.wbt` when present, otherwise falls back to `worlds/alien_mvp.wbt` for compatibility with the current MVP repository layout.

This deliberately invokes the Webots executable directly. Do **not** use macOS `open` on a `.wbt` file; that produces `kLSApplicationNotFoundErr` when no file association is registered.

## Demo controls

Use the keyboard in Webots:

- `G` — walk to the toy, grasp it, and return home
- `W` — walk home
- `F` — simulate a fall and recover
- `R` — continue recovery
- `H` — reset to standing/home

The controller also enables both camera eyes, IMU, gyro, accelerometer, range sensor, microphone and speaker devices. Voice recognition is intentionally represented by the ROS 2 `voice/command` interface in this slice; an STT adapter will be added next.

## Important MVP boundary

The current walking and recovery motion is a deterministic Supervisor demonstration. It is **not** yet a physically validated biped gait or whole-body controller. The next slice replaces scripted body motion with joint-level motors, balance feedback and contact-aware recovery.
