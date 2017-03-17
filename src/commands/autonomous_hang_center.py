import configparser
from wpilib.command import CommandGroup
from commands.drive_encoder_counts import DriveEncoderCounts
from commands.drive_time import DriveTime
from commands.abort_commands import Abort


class AutonomousHangCenter(CommandGroup):
    _approach_section = "Approach"
    _approach_speed_key = "APPROACH_SPEED"
    _approach_encoder_counts_key = "APPROACH_ENCODER_COUNTS"
    _approach_encoder_threshold_key = "APPROACH_ENCODER_THRESHOLD"
    _approach_time_key = "APPROACH_TIME"
    _initial_wait_time_key = "INITIAL_WAIT_TIME"

    _hang_section = "Hang"
    _hang_center_approach_speed_key = "HANG_CENTER_APPROACH_SPEED"
    _hang_center_approach_time_key = "HANG_CENTER_APPROACH_TIME"

    _robot = None
    _config = None
    _default_timeout = 15

    _starting_position = None

    _approach_speed = None
    _approach_encoder_counts = None
    _approach_encoder_threshold = None
    _approach_time = None
    _initial_wait_time = None

    _hang_center_approach_speed = None
    _hang_center_approach_time = None

    def __init__(self, robot, configfile="/home/lvuser/py/configs/autonomous.ini"):
        super().__init__()
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_commands()

    def set_match_configuration(self, starting_position):
        self._starting_position = starting_position
        self._add_approach_commands(self._robot.drivetrain.is_encoder_enabled(),
                                    self._robot.drivetrain.is_gyro_enabled())
        self._add_hang_center_commands(self._robot.drivetrain.is_encoder_enabled(),
                                       self._robot.drivetrain.is_gyro_enabled())

        # abort all commands as the last command
        self.addSequential(Abort(self._robot))

    def _init_commands(self):
        self._approach_speed = self._config.getfloat(AutonomousHangCenter._approach_section,
                                                     AutonomousHangCenter._approach_speed_key)
        self._approach_encoder_counts = self._config.getint(AutonomousHangCenter._approach_section,
                                                            AutonomousHangCenter._approach_encoder_counts_key)
        self._approach_encoder_threshold = self._config.getint(AutonomousHangCenter._approach_section,
                                                               AutonomousHangCenter._approach_encoder_threshold_key)
        self._approach_time = self._config.getfloat(AutonomousHangCenter._approach_section,
                                                    AutonomousHangCenter._approach_time_key)
        self._initial_wait_time = self._config.getfloat(AutonomousHangCenter._approach_section,
                                                        AutonomousHangCenter._initial_wait_time_key)

        self._hang_center_approach_speed = self._config.getfloat(AutonomousHangCenter._hang_section,
                                                                 AutonomousHangCenter._hang_center_approach_speed_key)
        self._hang_center_approach_time = self._config.getfloat(AutonomousHangCenter._hang_section,
                                                                AutonomousHangCenter._hang_center_approach_time_key)

    def _add_approach_commands(self, use_encoder=False, use_gyro=False):
        approach_commands = CommandGroup()
        approach_commands.addSequential(DriveTime(self._robot, self._initial_wait_time, 0.0), self._default_timeout)
        # Drive up to the tower, just before the line
        if use_encoder:
            approach_commands.addSequential(DriveEncoderCounts(self._robot, self._approach_encoder_counts,
                                                               self._approach_speed,
                                                               self._approach_encoder_threshold),
                                            self._default_timeout)
        else:
            approach_commands.addSequential(DriveTime(self._robot, self._approach_time, self._approach_speed),
                                            self._default_timeout)
        self.addSequential(approach_commands)

    def _add_hang_center_commands(self, use_encoder=False, use_gyro=False):
        hang_commands = CommandGroup()
        hang_commands.addSequential(DriveTime(self._robot, self._hang_center_approach_time,
                                              self._hang_center_approach_speed), self._default_timeout)
        self.addSequential(hang_commands)

    def initialize(self):
        pass  # Can be overwritten by teams

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
