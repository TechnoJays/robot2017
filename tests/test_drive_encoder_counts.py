import pytest
from commands.drive_encoder_counts import DriveEncoderCounts
from subsystems.drivetrain import Drivetrain


"""
hal_data['pwm'] looks like this:
[{
    'zero_latch': False,
    'initialized': False,
    'raw_value': 0,
    'value': 0,
    'period_scale': None,
    'type': None
}, {
    'zero_latch': True,
    'initialized': True,
    'raw_value': 1011,
    'value': 0.0,
    'period_scale': 0,
    'type': 'talon'
},...]
"""


@pytest.fixture(scope="function")
def drivetrain_default(robot):
    return Drivetrain(robot, None, '../tests/test_configs/drivetrain_default.ini')


@pytest.fixture(scope="function")
def command_default(robot, drivetrain_default):
    robot.drivetrain = drivetrain_default
    return DriveEncoderCounts(robot, 500.0, 1.0, 50.0, None, 15)


def update_encoders(hal_data, command):
    current_0 = hal_data['encoder'][0]['count']
    counts_left = command._target_position - current_0
    if counts_left >= 0:
        hal_data['encoder'][0]['count'] += 1
        hal_data['encoder'][1]['count'] += 1
    else:
        hal_data['encoder'][0]['count'] -= 1
        hal_data['encoder'][1]['count'] -= 1


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.drivetrain is not None
    assert command_default.name == "DriveEncoderCounts"
    assert command_default.timeout == 15
    assert command_default._speed == 1.0
    assert command_default._encoder_change == 500.0
    assert command_default._encoder_threshold == 50.0


def test_init_full(robot, drivetrain_default):
    robot.drivetrain = drivetrain_default
    dec = DriveEncoderCounts(robot, 10000.0, 0.5, 10.0, "CustomDriveEncoderCounts", 5)
    assert dec is not None
    assert dec.robot is not None
    assert dec.robot.drivetrain is not None
    assert dec.name == "CustomDriveEncoderCounts"
    assert dec.timeout == 5
    assert dec._speed == 0.5
    assert dec._encoder_change == 10000.0
    assert dec._encoder_threshold == 10.0


def test_initialize(command_default):
    command_default.initialize()
    assert command_default._target_position == 500


@pytest.mark.parametrize("initial_count,count_change,threshold,speed,left_ex_speed,right_ex_speed", [
    (0, 0, 5, 1.0, -1.0, 1.0),
    (100, 400, 10, 1.0, -1.0, 1.0),
    (500, 9500, 50, 0.5, -0.5, 0.5),
    (10000, -5000, 100, 1.0, 1.0, -1.0),
    (500, -500, 2, 0.5, 0.5, -0.5),
])
def test_execute(robot, drivetrain_default, hal_data, initial_count, count_change, threshold, speed,
                 left_ex_speed, right_ex_speed):
    robot.drivetrain = drivetrain_default
    dec = DriveEncoderCounts(robot, count_change, speed, threshold, "CustomDriveEncoderCounts", 15)
    assert dec is not None
    hal_data['encoder'][0]['count'] = initial_count
    hal_data['encoder'][1]['count'] = initial_count
    dec.initialize()
    dec.execute()
    assert hal_data['pwm'][1]['value'] == left_ex_speed
    assert hal_data['pwm'][2]['value'] == right_ex_speed


@pytest.mark.parametrize("initial_count,count_change,threshold,fake_count,finished", [
    (0, 0, 5, 0, True),
    (100, 400, 10, 489, False),
    (500, 9500, 50, 9951, True),
    (10000, -5000, 100, 5101, False),
    (500, -500, 2, 1, True),
])
def test_is_finished(robot, drivetrain_default, hal_data, initial_count, count_change, threshold, fake_count, finished):
    robot.drivetrain = drivetrain_default
    dec = DriveEncoderCounts(robot, count_change, 1.0, threshold, "CustomDriveEncoderCounts", 15)
    assert dec is not None
    hal_data['encoder'][0]['count'] = initial_count
    hal_data['encoder'][1]['count'] = initial_count
    dec.initialize()
    hal_data['encoder'][0]['count'] = fake_count
    hal_data['encoder'][1]['count'] = fake_count
    assert dec.isFinished() is finished


def test_interrupted(command_default):
    pass  # interrupted method is empty


def test_end(command_default, hal_data):
    assert hal_data['pwm'][1]['value'] == 0.0
    assert hal_data['pwm'][2]['value'] == 0.0


@pytest.mark.parametrize("initial_count,count_change,threshold,speed,left_ex_speed,right_ex_speed", [
    (0, 0, 5, 1.0, -1.0, 1.0),
    (100, 400, 10, 1.0, -1.0, 1.0),
    (500, 9500, 50, 0.5, -0.5, 0.5),
    (10000, -5000, 100, 1.0, 1.0, -1.0),
    (500, -500, 2, 0.5, 0.5, -0.5),
])
def test_command_full(robot, drivetrain_default, hal_data, initial_count, count_change, threshold, speed,
                 left_ex_speed, right_ex_speed):
    robot.drivetrain = drivetrain_default
    dec = DriveEncoderCounts(robot, count_change, speed, threshold, "CustomDriveEncoderCounts", 15)
    assert dec is not None
    hal_data['encoder'][0]['count'] = initial_count
    hal_data['encoder'][1]['count'] = initial_count
    dec.initialize()
    while not dec.isFinished():
        dec.execute()
        update_encoders(hal_data, dec)
        assert hal_data['pwm'][1]['value'] == left_ex_speed
        assert hal_data['pwm'][2]['value'] == right_ex_speed
    dec.end()
    assert isclose(hal_data['encoder'][0]['count'], initial_count + count_change, threshold)
    assert isclose(hal_data['encoder'][1]['count'], initial_count + count_change, threshold)
