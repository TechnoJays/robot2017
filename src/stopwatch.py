import time


class Stopwatch(object):
    """Provides stopwatch timing functionality.

    This class provides simple time keeping functionality like a stopwatch.

    """
    _running = False
    _start = None
    _end = None
    _secs = None
    _msecs = None

    def __init__(self):
        """Create and initialize a Stopwatch."""
        self._start = None
        self._end = None
        self._secs = None
        self._msecs = None
        self._running = False

    def start(self):
        """Mark current time as the starting time."""
        self._start = time.time()
        self._running = True
        self._end = None
        self._secs = None
        self._msecs = None

    def reset(self):
        """Reset the timer to zero.

        This doesn't stop the timer, but simply moves the starting
        time to the current time and clears the end and elapses times.

        """
        self._start = time.time()
        self._end = None
        self._secs = None
        self._msecs = None

    def stop(self):
        """Mark current time as ending time and calculate duration.

        If the stopwatch has been started, mark the current time as the end time
        and calculate the time difference between the start and end points in
        both seconds and milliseconds.  If the stopwatch was never started, do
        nothing.

        """
        if self._running:
            self._end = time.time()
            self._running = False

    def elapsed_time_in_secs(self):
        """Return elapsed time in seconds.

        Calculate the time difference between the start and end times in
        seconds. If the stopwatch is currently running, the current time is used
        as the end time.  If the stopwatch was never started, return None.

        """
        if self._running:
            self._end = time.time()
        if self._start and self._end:
            self._secs = self._end - self._start
        return self._secs

    def elapsed_time_in_msecs(self):
        """Return elapsed time in milliseconds.

        Calculate the time difference between the start and end times in
        milliseconds.  If the stopwatch is currently running, the current time
        is used as the end time.  If the stopwatch was never started,
        return None.

        """

        secs = self.elapsed_time_in_secs()
        if secs:
            self._msecs = secs * 1000
        return self._msecs
