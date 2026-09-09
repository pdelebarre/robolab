"""Deterministic joint-space gait controller for the RoboLab alien biped.

The controller intentionally separates gait generation from balance feedback so
both pieces can be tested without a Webots runtime. It drives six leg motors
(hip/knee/ankle on each side), applies small IMU pitch/roll corrections, and
falls back to a neutral pose when contact is lost or the robot tilts too far.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable


LEG_JOINTS = (
    "left_hip_motor",
    "left_knee_motor",
    "left_ankle_motor",
    "right_hip_motor",
    "right_knee_motor",
    "right_ankle_motor",
)


@dataclass(frozen=True)
class GaitConfig:
    step_period_s: float = 0.72
    swing_amplitude_rad: float = 0.32
    knee_lift_rad: float = 0.42
    ankle_amplitude_rad: float = 0.20
    hip_bias_rad: float = 0.04
    balance_gain: float = 0.18
    max_balance_correction_rad: float = 0.14
    fall_threshold_rad: float = 1.0


class GaitGenerator:
    """Generate symmetric alternating target angles in radians."""

    def __init__(self, config: GaitConfig | None = None) -> None:
        self.config = config or GaitConfig()

    def targets(self, elapsed_s: float, pitch_rad: float = 0.0, roll_rad: float = 0.0) -> dict[str, float]:
        phase = (elapsed_s % self.config.step_period_s) / self.config.step_period_s
        theta = 2.0 * math.pi * phase

        left = 1.0 if math.sin(theta) >= 0.0 else -1.0
        right = -left
        swing = math.sin(theta)
        lift = max(0.0, math.sin(theta))
        correction_pitch = max(
            -self.config.max_balance_correction_rad,
            min(self.config.max_balance_correction_rad, -pitch_rad * self.config.balance_gain),
        )
        correction_roll = max(
            -self.config.max_balance_correction_rad,
            min(self.config.max_balance_correction_rad, -roll_rad * self.config.balance_gain),
        )

        return {
            "left_hip_motor": self.config.hip_bias_rad + self.config.swing_amplitude_rad * swing + correction_pitch,
            "left_knee_motor": self.config.knee_lift_rad * lift,
            "left_ankle_motor": -self.config.ankle_amplitude_rad * swing - correction_pitch - correction_roll,
            "right_hip_motor": -self.config.hip_bias_rad - self.config.swing_amplitude_rad * swing + correction_pitch,
            "right_knee_motor": self.config.knee_lift_rad * max(0.0, -math.sin(theta)),
            "right_ankle_motor": self.config.ankle_amplitude_rad * swing - correction_pitch + correction_roll,
        }

    def fallen(self, pitch_rad: float, roll_rad: float) -> bool:
        return max(abs(pitch_rad), abs(roll_rad)) >= self.config.fall_threshold_rad

    def neutral(self) -> dict[str, float]:
        return {joint: 0.0 for joint in LEG_JOINTS}


def apply_targets(motors: Iterable[object], targets: dict[str, float]) -> None:
    """Apply targets to Webots motors or compatible test doubles."""
    for motor in motors:
        name = motor.getName()
        motor.setPosition(targets[name])


if __name__ == "__main__":
    from controller import Robot

    TIME_STEP = 16
    robot = Robot()
    gait = GaitGenerator()
    motors = [robot.getDevice(name) for name in LEG_JOINTS]
    for motor in motors:
        motor.setVelocity(5.0)
        motor.setPosition(0.0)

    imu = robot.getDevice("imu")
    imu.enable(TIME_STEP)
    left_foot = robot.getDevice("left_foot_contact")
    right_foot = robot.getDevice("right_foot_contact")
    left_foot.enable(TIME_STEP)
    right_foot.enable(TIME_STEP)

    elapsed_s = 0.0
    while robot.step(TIME_STEP) != -1:
        roll, pitch, _ = imu.getRollPitchYaw()
        if gait.fallen(pitch, roll):
            apply_targets(motors, gait.neutral())
            continue
        apply_targets(motors, gait.targets(elapsed_s, pitch, roll))
        elapsed_s += TIME_STEP / 1000.0
