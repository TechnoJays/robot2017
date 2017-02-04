import pytest
from subsystems.drivetrain import Drivetrain

'''
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
'''


@pytest.fixture(scope="function")
def drivetrain_default(robot):
    return Drivetrain(robot, None, '../tests/test_configs/drivetrain_default.ini')


def test_drivetrain_default(drivetrain_default, hal_data):
    assert drivetrain_default is not None
    assert drivetrain_default._left_motor is not None
    assert drivetrain_default._right_motor is not None
    assert drivetrain_default._robot_drive is not None


def test_drivetrain_channels_0_1(hal_data, robot):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_channels_0_1.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert hal_data['pwm'][0]['initialized'] is True
    assert hal_data['pwm'][0]['value'] == 0.0
    assert hal_data['pwm'][0]['type'] == 'talon'
    assert hal_data['pwm'][0]['zero_latch'] is True
    assert hal_data['pwm'][1]['initialized'] is True
    assert hal_data['pwm'][1]['value'] == 0.0
    assert hal_data['pwm'][1]['type'] == 'talon'
    assert hal_data['pwm'][1]['zero_latch'] is True
    assert hal_data['pwm'][2]['initialized'] is False


def test_drivetrain_channels_1_2(hal_data, robot):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_channels_1_2.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert hal_data['pwm'][0]['initialized'] is False
    assert hal_data['pwm'][1]['initialized'] is True
    assert hal_data['pwm'][1]['value'] == 0.0
    assert hal_data['pwm'][1]['type'] == 'talon'
    assert hal_data['pwm'][1]['zero_latch'] is True
    assert hal_data['pwm'][2]['initialized'] is True
    assert hal_data['pwm'][2]['value'] == 0.0
    assert hal_data['pwm'][2]['type'] == 'talon'
    assert hal_data['pwm'][2]['zero_latch'] is True
    assert hal_data['pwm'][3]['initialized'] is False


@pytest.mark.parametrize("left_speed,right_speed,left_ex_speed,right_ex_speed", [
    (0.0, 0.0, 0.0, 0.0),
    (0.5, 0.5, 0.0, 0.0),
    (1.0, 1.0, 0.0, 0.0),
    (-0.5, -0.5, 0.0, 0.0),
    (-1.0, -1.0, 0.0, 0.0),
])
def test_drivetrain_zero_speed(hal_data, robot, left_speed, right_speed, left_ex_speed, right_ex_speed):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_zero_speed.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert dt._max_speed == 0.0
    dt.tank_drive(left_speed, right_speed)
    assert hal_data['pwm'][1]['value'] == left_ex_speed
    assert hal_data['pwm'][2]['value'] == right_ex_speed


@pytest.mark.parametrize("left_speed,right_speed,left_ex_speed,right_ex_speed", [
    (0.0, 0.0, 0.0, 0.0),
    (0.5, 0.5, 0.25, -0.25),
    (1.0, 1.0, 0.5, -0.5),
    (-0.5, -0.5, -0.25, 0.25),
    (-1.0, -1.0, -0.5, 0.5),
])
def test_drivetrain_half_speed(hal_data, robot, left_speed, right_speed, left_ex_speed, right_ex_speed):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_half_speed.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert dt._max_speed == 0.5
    dt.tank_drive(left_speed, right_speed)
    assert abs(hal_data['pwm'][1]['value']) - abs(left_ex_speed) < 0.05
    assert abs(hal_data['pwm'][2]['value']) - abs(right_ex_speed) < 0.05


@pytest.mark.parametrize("left_speed,right_speed,left_ex_speed,right_ex_speed", [
    (0.0, 0.0, 0.0, 0.0),
    (0.5, 0.5, 0.375, -0.375),
    (1.0, 1.0, 0.75, -0.75),
    (-0.5, -0.5, -0.375, 0.375),
    (-1.0, -1.0, -0.75, 0.75),
])
def test_drivetrain_3_4_speed(hal_data, robot, left_speed, right_speed, left_ex_speed, right_ex_speed):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_3_4_speed.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert dt._max_speed == 0.75
    dt.tank_drive(left_speed, right_speed)
    assert abs(hal_data['pwm'][1]['value']) - abs(left_ex_speed) < 0.05
    assert abs(hal_data['pwm'][2]['value']) - abs(right_ex_speed) < 0.05


@pytest.mark.parametrize("left_speed,right_speed,left_ex_speed,right_ex_speed", [
    (0.0, 0.0, 0.0, 0.0),
    (0.5, 0.5, 0.5, -0.5),
    (1.0, 1.0, 1.0, -1.0),
    (-0.5, -0.5, -0.5, 0.5),
    (-1.0, -1.0, -1.0, 1.0),
])
def test_drivetrain_full_speed(hal_data, robot, left_speed, right_speed, left_ex_speed, right_ex_speed):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_full_speed.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert dt._max_speed == 1.0
    dt.tank_drive(left_speed, right_speed)
    assert hal_data['pwm'][1]['value'] == left_ex_speed
    assert hal_data['pwm'][2]['value'] == right_ex_speed


def test_drivetrain_left_inverted(hal_data, robot):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_left_inverted.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert hal_data['pwm'][1]['initialized'] is True
    assert hal_data['pwm'][1]['value'] == 0.0
    assert hal_data['pwm'][1]['type'] == 'talon'
    assert hal_data['pwm'][1]['zero_latch'] is True
    assert hal_data['pwm'][2]['initialized'] is True
    assert hal_data['pwm'][2]['value'] == 0.0
    assert hal_data['pwm'][2]['type'] == 'talon'
    assert hal_data['pwm'][2]['zero_latch'] is True
    assert dt._left_motor.getInverted() is True
    assert dt._right_motor.getInverted() is False


def test_drivetrain_right_inverted(hal_data, robot):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_right_inverted.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None
    assert hal_data['pwm'][1]['initialized'] is True
    assert hal_data['pwm'][1]['value'] == 0.0
    assert hal_data['pwm'][1]['type'] == 'talon'
    assert hal_data['pwm'][1]['zero_latch'] is True
    assert hal_data['pwm'][2]['initialized'] is True
    assert hal_data['pwm'][2]['value'] == 0.0
    assert hal_data['pwm'][2]['type'] == 'talon'
    assert hal_data['pwm'][2]['zero_latch'] is True
    assert dt._left_motor.getInverted() is False
    assert dt._right_motor.getInverted() is True


def test_drivetrain_left_disabled(hal_data, robot):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_left_disabled.ini')
    assert dt is not None
    assert dt._left_motor is None
    assert dt._right_motor is not None
    assert dt._robot_drive is None


def test_drivetrain_right_disabled(hal_data, robot):
    dt = Drivetrain(robot, None, '../tests/test_configs/drivetrain_right_disabled.ini')
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is None
    assert dt._robot_drive is None
