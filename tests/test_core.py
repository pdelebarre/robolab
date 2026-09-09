import unittest

from alien_robot.core import BehaviorManager, Robot, RobotState, SceneObject


class AlienRobotBehaviorTests(unittest.TestCase):
    def test_robot_dimension(self):
        self.assertEqual(Robot().height_m, 0.25)

    def test_walk_reaches_target(self):
        robot = Robot()
        for _ in range(100):
            robot.walk_towards((0.4, 0.0))
        self.assertAlmostEqual(robot.pose.x, 0.4, places=3)

    def test_fall_detection_and_recovery(self):
        robot = Robot()
        self.assertTrue(robot.detect_fall(1.1))
        self.assertEqual(robot.state, RobotState.FALLEN)
        robot.start_recovery()
        for _ in range(4):
            robot.recovery_step()
        self.assertEqual(robot.state, RobotState.STANDING)
        self.assertEqual(robot.fallen_angle_rad, 0.0)

    def test_grasp_nearby_object(self):
        robot = Robot()
        scene = {"ball": SceneObject("ball", 0.03, 0.0)}
        behavior = BehaviorManager(robot, scene)
        result = behavior.tick_pick_and_carry((0.5, 0.0))
        self.assertEqual(result, "grasped")
        self.assertEqual(robot.carrying, "ball")
        self.assertTrue(scene["ball"].held)

    def test_no_object(self):
        behavior = BehaviorManager(Robot(), {})
        self.assertEqual(behavior.tick_pick_and_carry((0.0, 0.0)), "no_object")


if __name__ == "__main__":
    unittest.main()
