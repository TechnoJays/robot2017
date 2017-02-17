import pytest
import oi
from subsystems.winch import Winch
from commands.activate_winch import ActivateWinch

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


@pytest.fixture(scope="function")
def command_default(robot, winch_default):
    robot.winch = winch_default
    return ActivateWinch(robot, None, None)


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.winch is not None
    assert command_default.name == "ActivateWinch"
    assert command_default.timeout is None


def test_init_full(robot, winch_default):
    robot.winch = winch_default
    mwa = ActivateWinch(robot, "CustomActivateWinch", 5)
    assert mwa is not None
    assert mwa.robot is not None
    assert mwa.robot.winch is not None
    assert mwa.name == "CustomActivateWinch"
    assert mwa.timeout == 5


def test_initialize(command_default):
    pass  # initialize method is empty


def test_execute(winch_default, robot, hal_data):
    robot.winch = winch_default
    mwa = ActivateWinch(robot, None, None)
    assert mwa is not None
    mwa.initialize()
    mwa.execute()
    assert hal_data['pwm'][3]['value'] == 1.0


def test_is_finished(command_default):
    assert command_default.isFinished() is False


def test_interrupted(command_default):
    pass  # interrupted method is empty


def test_end(winch_default, robot, hal_data):
    robot.winch = winch_default
    mwa = ActivateWinch(robot, None, None)
    assert mwa is not None
    mwa.initialize()
    mwa.execute()
    mwa.end()
    assert hal_data['pwm'][3]['value'] == 0.0
