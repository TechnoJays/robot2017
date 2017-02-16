import configparser
from wpilib.command import CommandGroup
from commands.drive_encoder_counts import DriveEncoderCounts


class AutonomousDefault(CommandGroup):
    _approach_section = "Approach"
    _approach_speed_key = "EncoderCounts"
    _approach_encoder_counts_key = "EncoderCounts"
    _approach_encoder_threshold_key = "EncoderCounts"

    _robot = None
    _config = None
    _default_timeout = 15

    _approach_commands = CommandGroup()
    _approach_speed = None
    _approach_encoder_counts = None
    _approach_encoder_threshold = None

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

    def _init_commands(self):
        self._approach_speed = self._config.getint(AutonomousDefault._approach_section,
                                                   AutonomousDefault._approach_speed_key)
        self._approach_encoder_counts = self._config.getint(AutonomousDefault._approach_section,
                                                            AutonomousDefault._approach_encoder_counts_key)
        self._approach_encoder_threshold = self._config.getint(AutonomousDefault._approach_section,
                                                               AutonomousDefault._approach_encoder_threshold_key)

    def _add_approach_commands(self):
        self._approach_commands.addSequential(DriveEncoderCounts(self._robot, self._approach_encoder_counts_key,
                                                                 self._approach_speed_key,
                                                                 self._approach_encoder_threshold_key),
                                              self._default_timeout)
        self.addSequential(self._approach_commands)

    def initialize(self):
        pass  # Can be overwritten by teams

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.drivetrain.arcade_drive(0, 0)
        self._robot.winch.move_winch(0.0)
        self._robot.gear_release.set_gear_release(False)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
