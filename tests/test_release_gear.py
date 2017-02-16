import pytest
from subsystems.gear_release import GearRelease
from commands.release_gear import ReleaseGear
import oi


@pytest.fixture(scope="function")
def gear_release_default(robot):
    return GearRelease(robot, None, '../tests/test_configs/gear_release_default.ini')


@pytest.fixture(scope="function")
def command_default(robot, gear_release_default):
    robot.gear_release = gear_release_default
    return ReleaseGear(robot, None, 15)


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.gear_release is not None
    assert command_default.name == "ReleaseGear"
    assert command_default.timeout == 15


def test_init_full(robot, gear_release_default):
    robot.gear_release = gear_release_default
    rg = ReleaseGear(robot, "CustomReleaseGear", 5)
    assert rg is not None
    assert rg.robot is not None
    assert rg.robot.gear_release is not None
    assert rg.name == "CustomReleaseGear"
    assert rg.timeout == 5


def test_initialize(command_default):
    pass  # initialize method is empty


def test_execute(robot, hal_data, gear_release_default):
    robot.gear_release = gear_release_default
    rg = ReleaseGear(robot, None, None)
    assert rg is not None
    rg.initialize()
    rg.execute()
    assert hal_data['solenoid'][0]['value'] is True


def test_is_finished(command_default):
    assert command_default.isFinished() is False


def test_interrupted(command_default):
    pass  # interrupted method is empty


def test_end(robot, hal_data, gear_release_default):
    robot.gear_release = gear_release_default
    rg = ReleaseGear(robot, None, None)
    assert rg is not None
    rg.initialize()
    rg.execute()
    rg.end()
    assert hal_data['solenoid'][0]['value'] is False
