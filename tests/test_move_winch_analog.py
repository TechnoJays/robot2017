import pytest
import oi
from subsystems.winch import Winch
from commands.move_winch_analog import MoveWinchAnalog

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
def mock_oi(robot):
    class OI:
        driver_values = {oi.JoystickAxis.LEFTX: 0.0, oi.JoystickAxis.LEFTY: 0.0,
                         oi.JoystickAxis.RIGHTX: 0.0, oi.JoystickAxis.RIGHTY: 0.0,
                         oi.JoystickAxis.DPADX: 0.0, oi.JoystickAxis.DPADY: 0.0}
        scoring_values = {oi.JoystickAxis.LEFTX: 0.0, oi.JoystickAxis.LEFTY: 0.0,
                         oi.JoystickAxis.RIGHTX: 0.0, oi.JoystickAxis.RIGHTY: 0.0,
                         oi.JoystickAxis.DPADX: 0.0, oi.JoystickAxis.DPADY: 0.0}
        values = {oi.UserController.DRIVER: driver_values,
                  oi.UserController.SCORING: scoring_values}

        def set_mock_axis_value(self, controller, axis, value):
            self.values[controller][axis] = value

        def get_axis(self, controller, axis):
            return self.values[controller][axis]
    return OI()


@pytest.fixture(scope="function")
def command_default(robot, winch_default):
    robot.winch = winch_default
    return MoveWinchAnalog(robot, None, None)


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.winch is not None
    assert command_default.name == "MoveWinchAnalog"
    assert command_default.timeout is None


def test_init_full(robot, winch_default):
    robot.winch = winch_default
    mwa = MoveWinchAnalog(robot, "CustomMoveWinchAnalog", 5)
    assert mwa is not None
    assert mwa.robot is not None
    assert mwa.robot.winch is not None
    assert mwa.name == "CustomMoveWinchAnalog"
    assert mwa.timeout == 5


def test_initialize(command_default):
    pass  # initialize method is empty


@pytest.mark.parametrize("speed,ex_speed", [
    (0.0, 0.0),
    (0.5, 0.5),
    (1.0, 1.0),
    (-0.5, -0.5),
    (-1.0, -1.0),
])
def test_execute(mock_oi, winch_default, robot, hal_data, speed, ex_speed):
    robot.winch = winch_default
    robot.oi = mock_oi
    mwa = MoveWinchAnalog(robot, None, None)
    assert mwa is not None
    mwa.initialize()
    mock_oi.set_mock_axis_value(oi.UserController.SCORING, oi.JoystickAxis.RIGHTY, speed)
    mwa.execute()
    assert hal_data['pwm'][3]['value'] == ex_speed


def test_is_finished(command_default):
    assert command_default.isFinished() is False


def test_interrupted(command_default):
    pass  # interrupted method is empty


def test_end(command_default):
    pass  # end method is empty
