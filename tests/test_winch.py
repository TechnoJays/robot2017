import pytest
from subsystems.winch import Winch

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
def winch_default(robot):
    return Winch(robot, None, '../tests/test_configs/winch_default.ini')


def test_winch_default(winch_default):
    assert winch_default is not None
    assert winch_default._motor is not None


def test_winch_channel_4(robot, hal_data):
    wnch = Winch(robot, None, '../tests/test_configs/winch_channel_4.ini')
    assert wnch is not None
    assert wnch._motor is not None
    print(hal_data)
    assert hal_data['pwm'][4]['initialized'] is True
    assert hal_data['pwm'][4]['value'] == 0.0
    assert hal_data['pwm'][4]['type'] == 'spark'


def test_winch_channel_5(robot, hal_data):
    wnch = Winch(robot, None, '../tests/test_configs/winch_channel_5.ini')
    assert wnch is not None
    assert wnch._motor is not None
    assert hal_data['pwm'][5]['initialized'] is True
    assert hal_data['pwm'][5]['value'] == 0.0
    assert hal_data['pwm'][5]['type'] == 'spark'


@pytest.mark.parametrize("speed,ex_speed", [
    (0.0, 0.0),
    (0.5, 0.5),
    (1.0, 1.0),
    (-0.5, -0.5),
    (-1.0, -1.0),
])
def test_winch_full_speed(robot, hal_data, speed, ex_speed):
    wnch = Winch(robot, None, '../tests/test_configs/winch_default.ini')
    assert wnch is not None
    assert wnch._motor is not None
    wnch.move_winch(speed)
    assert hal_data['pwm'][3]['value'] == ex_speed


def test_winch_inverted(robot, hal_data):
    wnch = Winch(robot, None, '../tests/test_configs/winch_inverted.ini')
    assert wnch is not None
    assert wnch._motor is not None
    assert hal_data['pwm'][3]['initialized'] is True
    assert hal_data['pwm'][3]['value'] == 0.0
    assert hal_data['pwm'][3]['type'] == 'spark'
    assert wnch._motor.getInverted() is True


def test_winch_disabled(robot):
    wnch = Winch(robot, None, '../tests/test_configs/winch_disabled.ini')
    assert wnch is not None
    assert wnch._motor is None
