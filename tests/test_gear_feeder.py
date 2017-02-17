import pytest
from subsystems.gear_feeder import GearFeeder

"""
hal_data['solenoid'] looks like this:
[{
      {
         'initialized':False,
         'value':None
      },
...]
"""


@pytest.fixture(scope="function")
def gear_feeder_default(robot):
    return GearFeeder(robot, None, '../tests/test_configs/gear_feeder_default.ini')


def test_gear_feeder_default(gear_feeder_default):
    assert gear_feeder_default is not None
    assert gear_feeder_default._solenoid is not None


def test_gear_feeder_channel_1(robot, hal_data):
    gr = GearFeeder(robot, None, '../tests/test_configs/gear_feeder_channel_1.ini')
    assert gr is not None
    assert gr._solenoid is not None
    assert hal_data['solenoid'][1]['initialized'] is True
    assert hal_data['solenoid'][1]['value'] == 0.0


def test_gear_feeder_channel_2(robot, hal_data):
    gr = GearFeeder(robot, None, '../tests/test_configs/gear_feeder_channel_2.ini')
    assert gr is not None
    assert gr._solenoid is not None
    assert hal_data['solenoid'][2]['initialized'] is True
    assert hal_data['solenoid'][2]['value'] == 0.0


@pytest.mark.parametrize("state,ex_state", [
    (True, True),
    (False, False),
])
def test_set_gear_feeder(robot, hal_data, state, ex_state):
    gr = GearFeeder(robot, None, '../tests/test_configs/gear_feeder_default.ini')
    assert gr is not None
    assert gr._solenoid is not None
    gr.set_gear_release(state)
    assert hal_data['solenoid'][0]['value'] == ex_state


def test_gear_feeder_disabled(robot, hal_data):
    gr = GearFeeder(robot, None, '../tests/test_configs/gear_feeder_disabled.ini')
    assert gr is not None
    assert gr._solenoid is None
    assert hal_data['solenoid'][0]['initialized'] is False
