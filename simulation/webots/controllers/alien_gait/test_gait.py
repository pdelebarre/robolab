import math

from alien_gait import GaitConfig, GaitGenerator, LEG_JOINTS


def test_targets_are_deterministic():
    gait = GaitGenerator()
    assert gait.targets(0.25) == gait.targets(0.25)
    assert set(gait.targets(0.25)) == set(LEG_JOINTS)


def test_left_and_right_hip_are_opposite_around_zero():
    gait = GaitGenerator(GaitConfig(hip_bias_rad=0.0))
    targets = gait.targets(0.20)
    assert math.isclose(targets["left_hip_motor"], -targets["right_hip_motor"], abs_tol=1e-9)


def test_knee_lift_is_non_negative():
    gait = GaitGenerator()
    for time_s in [i * 0.01 for i in range(100)]:
        targets = gait.targets(time_s)
        assert targets["left_knee_motor"] >= 0.0
        assert targets["right_knee_motor"] >= 0.0


def test_balance_correction_is_bounded():
    gait = GaitGenerator(GaitConfig(balance_gain=1.0, max_balance_correction_rad=0.14))
    targets = gait.targets(0.2, pitch_rad=3.0, roll_rad=-3.0)
    assert abs(targets["left_hip_motor"]) <= 0.32 + 0.04 + 0.14 + 1e-9
    assert abs(targets["left_ankle_motor"]) <= 0.20 + 0.14 + 0.14 + 1e-9


def test_fall_detection_uses_pitch_or_roll():
    gait = GaitGenerator(GaitConfig(fall_threshold_rad=1.0))
    assert not gait.fallen(0.5, 0.2)
    assert gait.fallen(1.01, 0.0)
    assert gait.fallen(0.0, -1.01)


def test_neutral_pose_contains_all_motors():
    gait = GaitGenerator()
    assert gait.neutral() == {joint: 0.0 for joint in LEG_JOINTS}
