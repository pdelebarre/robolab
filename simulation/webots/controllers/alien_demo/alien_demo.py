from controller import Robot

TIME_STEP = 16
robot = Robot()

left_eye = robot.getDevice('left_eye')
right_eye = robot.getDevice('right_eye')
left_eye.enable(TIME_STEP)
right_eye.enable(TIME_STEP)

imu = robot.getDevice('imu')
imu.enable(TIME_STEP)
range_sensor = robot.getDevice('front_range')
range_sensor.enable(TIME_STEP)

speaker = robot.getDevice('speaker')
speaker.speak('Hello! I am RoboLab Alien.', 1.0)

# This controller intentionally demonstrates the sensor/audio loop while the
# articulated gait controller is developed in the next slice.
while robot.step(TIME_STEP) != -1:
    orientation = imu.getRollPitchYaw()
    distance = range_sensor.getValue()
    if abs(orientation[0]) > 1.0 or abs(orientation[1]) > 1.0:
        speaker.speak('I fell. Recovering!', 1.0)
