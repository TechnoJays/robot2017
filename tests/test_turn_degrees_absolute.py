import pytest
from commands.turn_degrees_absolute import TurnDegreesAbsolute
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
    return TurnDegreesAbsolute(robot, 90.0, 1.0, 2.0, None, 15)


def update_gyro(hal_data, command):
    current = hal_data['analog_gyro'][1]['angle']
    degrees_left = command._target_degrees - current
    if degrees_left >= 0:
        hal_data['analog_gyro'][1]['angle'] += 1.0
    else:
        hal_data['analog_gyro'][1]['angle'] -= 1.0


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.drivetrain is not None
    assert command_default.name == "TurnDegreesAbsolute"
    assert command_default.timeout == 15
    assert command_default._target_degrees == 90.0
    assert command_default._speed == 1.0
    assert command_default._degree_threshold == 2.0


def test_init_full(robot, drivetrain_default):
    robot.drivetrain = drivetrain_default
    td = TurnDegreesAbsolute(robot, -30.0, 0.5, 5.0, "CustomTurnDegreesAbsolute", 5)
    assert td is not None
    assert td.robot is not None
    assert td.robot.drivetrain is not None
    assert td.name == "CustomTurnDegreesAbsolute"
    assert td.timeout == 5
    assert td._target_degrees == -30.0
    assert td._speed == 0.5
    assert td._degree_threshold == 5.0


def test_initialize(command_default):
    pass


@pytest.mark.parametrize("initial_angle,target_angle,threshold,speed,left_ex_speed,right_ex_speed", [
    (0.0, 0.0, 1.0, 1.0, -1.0, -1.0),
    (10.0, 30.0, 2.0, 1.0, -1.0, -1.0),
    (20.0, 60.0, 5.0, 0.5, -0.5, -0.5),
    (20.0, -60.0, 10.0, 1.0, 1.0, 1.0),
    (10.0, -30.0, 2.0, 0.5, 0.5, 0.5),
])
def test_execute(robot, drivetrain_default, hal_data, initial_angle, target_angle, threshold, speed,
                 left_ex_speed, right_ex_speed):
    robot.drivetrain = drivetrain_default
    td = TurnDegreesAbsolute(robot, target_angle, speed, threshold, "CustomTurnDegreesAbsolute", 15)
    assert td is not None
    hal_data['analog_gyro'][1]['angle'] = initial_angle
    td.initialize()
    td.execute()
    assert hal_data['pwm'][1]['value'] == left_ex_speed
    assert hal_data['pwm'][2]['value'] == right_ex_speed


@pytest.mark.parametrize("initial_angle,target_angle,threshold,fake_angle,finished", [
    (0.0, 0.0, 1.0, 0.0, True),
    (10.0, 30.0, 2.0, 27.0, False),
    (20.0, 60.0, 5.0, 56.0, True),
    (20.0, -60.0, 10.0, -49.0, False),
    (10.0, -30.0, 2.0, -29.0, True),
])
def test_is_finished(robot, drivetrain_default, hal_data, initial_angle, target_angle, threshold, fake_angle, finished):
    robot.drivetrain = drivetrain_default
    td = TurnDegreesAbsolute(robot, target_angle, 1.0, threshold, "CustomTurnDegreesAbsolute", 15)
    assert td is not None
    hal_data['analog_gyro'][1]['angle'] = initial_angle
    td.initialize()
    hal_data['analog_gyro'][1]['angle'] = fake_angle
    assert td.isFinished() is finished


def test_interrupted(command_default):
    pass  # interrupted method is empty


def test_end(command_default, hal_data):
    assert hal_data['pwm'][1]['value'] == 0.0
    assert hal_data['pwm'][2]['value'] == 0.0


@pytest.mark.parametrize("initial_angle,target_angle,threshold,speed,left_ex_speed,right_ex_speed", [
    (0.0, 0.0, 1.0, 1.0, 0.0, 0.0),
    (10.0, 30.0, 2.0, 1.0, -1.0, -1.0),
    (20.0, 60.0, 5.0, 0.5, -0.5, -0.5),
    (20.0, -60.0, 10.0, 1.0, 1.0, 1.0),
    (10.0, -30.0, 2.0, 0.5, 0.5, 0.5),
])
def test_command_full(robot, drivetrain_default, hal_data, initial_angle, target_angle, threshold, speed,
                      left_ex_speed, right_ex_speed):
    robot.drivetrain = drivetrain_default
    td = TurnDegreesAbsolute(robot, target_angle, speed, threshold, "CustomTurnDegreesAbsolute", 15)
    assert td is not None
    hal_data['analog_gyro'][1]['angle'] = initial_angle
    td.initialize()
    while not td.isFinished():
        td.execute()
        update_gyro(hal_data, td)
        assert hal_data['pwm'][1]['value'] == left_ex_speed
        assert hal_data['pwm'][2]['value'] == right_ex_speed
    td.end()
    assert isclose(hal_data['analog_gyro'][1]['angle'], target_angle, threshold)
