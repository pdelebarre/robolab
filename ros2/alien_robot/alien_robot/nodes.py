import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from .core import BehaviorManager, Robot, SceneObject


class BehaviorNode(Node):
    def __init__(self) -> None:
        super().__init__("behavior_manager")
        self.robot = Robot()
        self.scene = {
            "toy": SceneObject("toy", 0.8, 0.0),
        }
        self.behavior = BehaviorManager(self.robot, self.scene)
        self.pub = self.create_publisher(String, "robot/state", 10)
        self.sub = self.create_subscription(String, "voice/command", self.command, 10)
        self.timer = self.create_timer(0.1, self.tick)
        self.target = (0.0, 0.0)

    def command(self, message: String) -> None:
        text = message.data.lower().strip()
        if "toy" in text or "object" in text or "ball" in text:
            self.target = (0.0, 0.0)
        elif "forward" in text:
            self.target = (1.0, self.robot.pose.y)
        elif "home" in text:
            self.target = (0.0, 0.0)

    def tick(self) -> None:
        if self.robot.carrying:
            self.behavior.tick_pick_and_carry(self.target)
        else:
            self.behavior.tick_pick_and_carry((0.0, 0.0))
        status = String()
        status.data = f"state={self.robot.state.value};x={self.robot.pose.x:.3f};y={self.robot.pose.y:.3f};carrying={self.robot.carrying or ''}"
        self.pub.publish(status)


def main() -> None:
    rclpy.init()
    node = BehaviorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
