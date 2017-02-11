import pytest
from commands.drive_time import DriveTime
from subsystems.drivetrain import Drivetrain
from stopwatch import Stopwatch


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
    return DriveTime(robot, 5, 1.0, None, None)


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.drivetrain is not None
    assert command_default._stopwatch is not None
    assert command_default.name == "DriveTime"
    assert command_default.timeout is None
    assert command_default._duration == 5
    assert command_default._speed == 1.0


def test_init_full(robot, drivetrain_default):
    robot.drivetrain = drivetrain_default
    dt = DriveTime(robot, 10, 0.5, "CustomDriveTime", 5)
    assert dt is not None
    assert dt.robot is not None
    assert dt.robot.drivetrain is not None
    assert dt._stopwatch is not None
    assert dt.name == "CustomDriveTime"
    assert dt.timeout == 5
    assert dt._duration == 10
    assert dt._speed == 0.5


def test_initialize(command_default):
    command_default.initialize()
    assert command_default._stopwatch._running


@pytest.mark.parametrize("speed,left_ex_speed,right_ex_speed", [
    (0.0, 0.0, 0.0),
    (0.5, 0.5, -0.5),
    (1.0, 1.0, -1.0),
    (-0.5, -0.5, 0.5),
    (-1.0, -1.0, 1.0),
])
def test_execute(robot, drivetrain_default, hal_data, speed, left_ex_speed, right_ex_speed):
    robot.drivetrain = drivetrain_default
    dt = DriveTime(robot, 5, speed, "CustomDriveTime", 15)
    assert dt is not None
    dt.execute()
    assert hal_data['pwm'][1]['value'] == left_ex_speed
    assert hal_data['pwm'][2]['value'] == right_ex_speed


def test_is_finished(command_default):
    command_default.initialize()
    assert command_default.isFinished() is False


def test_interrupted(command_default):
    pass  # interrupted method is empty


def test_end(command_default, hal_data):
    assert command_default._stopwatch._running is False
    assert hal_data['pwm'][1]['value'] == 0.0
    assert hal_data['pwm'][2]['value'] == 0.0


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


@pytest.mark.parametrize("duration,speed,timeout,left_ex_speed,right_ex_speed", [
    (1.0, 0.5, 5.0, 0.5, -0.5),
    (5.0, 1.0, 15.0, 1.0, -1.0),
    # (5.0, 1.0, 1.0, 1.0, -1.0), # Timeouts don't seem to work in testing
])
def test_command_full(robot, drivetrain_default, hal_data, duration, speed, timeout, left_ex_speed, right_ex_speed):
    robot.drivetrain = drivetrain_default
    dt = DriveTime(robot, duration, speed, "CustomDriveTime", timeout)
    sw = Stopwatch()
    assert dt is not None
    dt.initialize()
    sw.start()
    while not dt.isFinished():
        dt.execute()
        assert hal_data['pwm'][1]['value'] == left_ex_speed
        assert hal_data['pwm'][2]['value'] == right_ex_speed
    dt.end()
    sw.stop()
    if duration < timeout:
        assert isclose(sw.elapsed_time_in_secs(), duration)
    else:
        # TODO: Timeouts don't seem to work in testing?
        assert isclose(sw.elapsed_time_in_secs(), timeout)
