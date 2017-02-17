import pytest
from stopwatch import Stopwatch

@pytest.fixture(scope="function")
def stopwatch_default(robot):
    return Stopwatch()


def test_stopwatch_default(stopwatch_default):
    assert stopwatch_default is not None
    assert stopwatch_default._start is None
    assert stopwatch_default._end is None
    assert stopwatch_default._secs is None
    assert stopwatch_default._msecs is None
    assert stopwatch_default._running is False


def test_start(stopwatch_default):
    stopwatch_default.start()
    assert stopwatch_default._start is not None
    assert stopwatch_default._running is True
    assert stopwatch_default._end is None
    assert stopwatch_default._secs is None
    assert stopwatch_default._msecs is None


def test_reset(stopwatch_default):
    stopwatch_default.start()
    start_time = stopwatch_default._start
    stopwatch_default.reset()
    assert stopwatch_default._start is not None
    assert stopwatch_default._start != start_time
    assert stopwatch_default._running is True
    assert stopwatch_default._end is None
    assert stopwatch_default._secs is None
    assert stopwatch_default._msecs is None


@pytest.mark.parametrize("started", [
    True,
    False
])
def test_stop(stopwatch_default, started):
    if started:
        stopwatch_default.start()
    stopwatch_default.stop()
    if started:
        assert stopwatch_default._start is not None
        assert stopwatch_default._end is not None
    else:
        assert stopwatch_default._start is None
        assert stopwatch_default._end is None
    assert stopwatch_default._secs is None
    assert stopwatch_default._msecs is None
    assert stopwatch_default._running is False


@pytest.mark.parametrize("started", [
    True,
    False
])
def test_elapsed_time_in_secs(stopwatch_default, started):
    if started:
        stopwatch_default.start()
    time_in_sec = stopwatch_default.elapsed_time_in_secs()
    if started:
        assert stopwatch_default._start is not None
        assert stopwatch_default._end is not None
        assert stopwatch_default._running is True
        assert stopwatch_default._secs is not None
        assert time_in_sec is not None
    else:
        assert stopwatch_default._start is None
        assert stopwatch_default._end is None
        assert stopwatch_default._running is False
        assert stopwatch_default._secs is None
        assert time_in_sec is None
    assert stopwatch_default._msecs is None


@pytest.mark.parametrize("started", [
    True,
    False
])
def test_elapsed_time_in_msecs(stopwatch_default, started):
    if started:
        stopwatch_default.start()
    time_in_msec = stopwatch_default.elapsed_time_in_msecs()
    if started:
        assert stopwatch_default._start is not None
        assert stopwatch_default._end is not None
        assert stopwatch_default._running is True
        assert stopwatch_default._secs is not None
        assert stopwatch_default._msecs is not None
        assert time_in_msec is not None
        assert stopwatch_default._msecs == stopwatch_default._secs * 1000
    else:
        assert stopwatch_default._start is None
        assert stopwatch_default._end is None
        assert stopwatch_default._running is False
        assert stopwatch_default._secs is None
        assert stopwatch_default._msecs is None
        assert time_in_msec is None
