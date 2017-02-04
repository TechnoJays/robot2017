import pytest
import oi
from commands.tank_drive import TankDrive
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
def command_default(robot, drivetrain_def):
    robot.drivetrain = drivetrain_def
    return TankDrive(robot, None, None)


def test_init_default(command_def):
    assert command_def is not None
    assert command_def.robot is not None
    assert command_def.robot.drivetrain is not None
    assert command_def.name == "TankDrive"
    assert command_def.timeout is None


def test_init_full(robot, drivetrain_def):
    robot.drivetrain = drivetrain_def
    td = TankDrive(robot, "CustomTankDrive", 5)
    assert td is not None
    assert td.robot is not None
    assert td.robot.drivetrain is not None
    assert td.name == "CustomTankDrive"
    assert td.timeout == 5


def test_initialize(command_def):
    pass  # initialize method is empty


@pytest.mark.parametrize("left_speed,right_speed,left_ex_speed,right_ex_speed", [
    (0.0, 0.0, 0.0, 0.0),
    (0.5, 0.5, 0.5, -0.5),
    (1.0, 1.0, 1.0, -1.0),
    (-0.5, -0.5, -0.5, 0.5),
    (-1.0, -1.0, -1.0, 1.0),
])
def test_execute(mock_oi, drivetrain_def, robot, hal_data, left_speed, right_speed, left_ex_speed, right_ex_speed):
    robot.drivetrain = drivetrain_def
    robot.oi = mock_oi
    td = TankDrive(robot, None, None)
    assert td is not None
    mock_oi.set_mock_axis_value(oi.UserController.DRIVER, oi.JoystickAxis.LEFTY, left_speed)
    mock_oi.set_mock_axis_value(oi.UserController.DRIVER, oi.JoystickAxis.RIGHTY, right_speed)
    td.execute()
    assert hal_data['pwm'][1]['value'] == left_ex_speed
    assert hal_data['pwm'][2]['value'] == right_ex_speed


def test_is_finished(command_def):
    assert command_def.isFinished() is False


def test_interrupted(command_def):
    pass  # interrupted method is empty


def test_end(command_def):
    pass  # end method is empty
