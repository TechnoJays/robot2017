import configparser
from wpilib.command import CommandGroup
from commands.drive_encoder_counts import DriveEncoderCounts
from commands.drive_time import DriveTime
from commands.abort_commands import Abort


class AutonomousDefault(CommandGroup):
    _approach_section = "Approach"
    _approach_speed_key = "APPROACH_SPEED"
    _approach_encoder_counts_key = "APPROACH_ENCODER_COUNTS"
    _approach_encoder_threshold_key = "APPROACH_ENCODER_THRESHOLD"
    _approach_time_key = "APPROACH_TIME"

    _robot = None
    _config = None
    _default_timeout = 15

    _approach_commands = CommandGroup()
    _approach_speed = None
    _approach_encoder_counts = None
    _approach_encoder_threshold = None
    _approach_time = None

    _starting_position = None

    def __init__(self, robot, configfile="/home/lvuser/py/configs/autonomous.ini"):
        super().__init__()
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_commands()

    def set_match_configuration(self, starting_position):
        self._starting_position = starting_position
        self._add_approach_commands()

        # abort all commands as the last command
        self.addSequential(Abort(self._robot))

    def _init_commands(self):
        self._approach_speed = self._config.getint(AutonomousDefault._approach_section,
                                                   AutonomousDefault._approach_speed_key)
        self._approach_encoder_counts = self._config.getint(AutonomousDefault._approach_section,
                                                            AutonomousDefault._approach_encoder_counts_key)
        self._approach_encoder_threshold = self._config.getint(AutonomousDefault._approach_section,
                                                               AutonomousDefault._approach_encoder_threshold_key)
        self._approach_time = self._config.getint(AutonomousDefault._approach_section,
                                                  AutonomousDefault._approach_time_key)

    def _add_approach_commands(self):
        # self._approach_commands.addSequential(DriveEncoderCounts(self._robot, self._approach_encoder_counts_key,
        #                                                          self._approach_speed_key,
        #                                                          self._approach_encoder_threshold_key),
        #                                       self._default_timeout)
        self._approach_commands.addSequential(DriveTime(self._robot, self._approach_time, self._approach_speed),
                                              self._default_timeout)
        self.addSequential(self._approach_commands)

    def initialize(self):
        pass  # Can be overwritten by teams

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
