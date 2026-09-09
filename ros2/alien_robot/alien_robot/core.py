from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import hypot
from typing import Dict, Optional, Tuple


class RobotState(str, Enum):
    STANDING = "standing"
    WALKING = "walking"
    GRASPING = "grasping"
    CARRYING = "carrying"
    FALLEN = "fallen"
    RECOVERING = "recovering"


class RecoveryPhase(str, Enum):
    IDLE = "idle"
    ROLL = "roll"
    KNEEL = "kneel"
    PUSH_UP = "push_up"
    STAND = "stand"
    COMPLETE = "complete"


@dataclass
class Pose2D:
    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0


@dataclass
class Robot:
    height_m: float = 0.25
    pose: Pose2D = field(default_factory=Pose2D)
    state: RobotState = RobotState.STANDING
    battery: float = 1.0
    carrying: Optional[str] = None
    fallen_angle_rad: float = 0.0
    recovery_phase: RecoveryPhase = RecoveryPhase.IDLE

    def walk_towards(self, target: Tuple[float, float], step_m: float = 0.02) -> None:
        dx = target[0] - self.pose.x
        dy = target[1] - self.pose.y
        distance = hypot(dx, dy)
        if distance < 1e-9:
            self.state = RobotState.STANDING
            return
        scale = min(step_m / distance, 1.0)
        self.pose.x += dx * scale
        self.pose.y += dy * scale
        self.state = RobotState.WALKING
        self.battery = max(0.0, self.battery - 0.0001)

    def detect_fall(self, tilt_rad: float, threshold_rad: float = 0.75) -> bool:
        self.fallen_angle_rad = tilt_rad
        if abs(tilt_rad) >= threshold_rad:
            self.state = RobotState.FALLEN
            self.recovery_phase = RecoveryPhase.IDLE
            return True
        return False

    def start_recovery(self) -> None:
        if self.state != RobotState.FALLEN:
            return
        self.state = RobotState.RECOVERING
        self.recovery_phase = RecoveryPhase.ROLL

    def recovery_step(self) -> None:
        if self.state != RobotState.RECOVERING:
            return
        next_phase = {
            RecoveryPhase.ROLL: RecoveryPhase.KNEEL,
            RecoveryPhase.KNEEL: RecoveryPhase.PUSH_UP,
            RecoveryPhase.PUSH_UP: RecoveryPhase.STAND,
            RecoveryPhase.STAND: RecoveryPhase.COMPLETE,
        }
        self.recovery_phase = next_phase.get(self.recovery_phase, RecoveryPhase.COMPLETE)
        if self.recovery_phase == RecoveryPhase.COMPLETE:
            self.pose = Pose2D(self.pose.x, self.pose.y, self.pose.yaw)
            self.fallen_angle_rad = 0.0
            self.state = RobotState.STANDING
            self.recovery_phase = RecoveryPhase.IDLE


@dataclass
class SceneObject:
    object_id: str
    x: float
    y: float
    graspable: bool = True
    held: bool = False


class BehaviorManager:
    def __init__(self, robot: Robot, objects: Dict[str, SceneObject]):
        self.robot = robot
        self.objects = objects
        self.destination: Optional[Tuple[float, float]] = None

    def find_nearest_graspable(self) -> Optional[SceneObject]:
        candidates = [o for o in self.objects.values() if o.graspable and not o.held]
        if not candidates:
            return None
        return min(candidates, key=lambda o: hypot(o.x - self.robot.pose.x, o.y - self.robot.pose.y))

    def tick_pick_and_carry(self, target: Tuple[float, float]) -> str:
        if self.robot.carrying:
            self.destination = target
            self.robot.walk_towards(target)
            self.robot.state = RobotState.CARRYING
            return "carrying"
        obj = self.find_nearest_graspable()
        if obj is None:
            return "no_object"
        if hypot(obj.x - self.robot.pose.x, obj.y - self.robot.pose.y) > 0.06:
            self.robot.walk_towards((obj.x, obj.y))
            return "approaching"
        obj.held = True
        self.robot.carrying = obj.object_id
        self.robot.state = RobotState.GRASPING
        return "grasped"
