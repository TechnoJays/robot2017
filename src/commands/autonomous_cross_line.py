import configparser
from wpilib.command import CommandGroup
from commands.drive_encoder_counts import DriveEncoderCounts
from commands.drive_time import DriveTime
from commands.abort_commands import Abort
from commands.turn_degrees import TurnDegrees
from commands.turn_time import TurnTime


class AutonomousCrossLine(CommandGroup):
    _approach_section = "Approach"
    _approach_speed_key = "APPROACH_SPEED"
    _approach_encoder_counts_key = "APPROACH_ENCODER_COUNTS"
    _approach_encoder_threshold_key = "APPROACH_ENCODER_THRESHOLD"
    _approach_time_key = "APPROACH_TIME"
    _initial_wait_time_key = "INITIAL_WAIT_TIME"

    _cross_section = "Cross"
    _cross_encoder_threshold_key = "CROSS_ENCODER_THRESHOLD"
    _cross_angle_threshold_key = "CROSS_ANGLE_THRESHOLD"

    _cross_speed_key = "CROSS_SPEED"
    _cross_encoder_counts_key = "CROSS_ENCODER_COUNTS"
    _cross_time_key = "CROSS_TIME"

    _cross_center_turn_speed_key = "CROSS_CENTER_TURN_SPEED"
    _cross_center_turn_angle_key = "CROSS_CENTER_TURN_ANGLE"
    _cross_center_turn_time_key = "CROSS_CENTER_TURN_TIME"
    _cross_center_drive_speed_key = "CROSS_CENTER_DRIVE_SPEED"
    _cross_center_drive_encoder_counts_key = "CROSS_CENTER_DRIVE_ENCODER_COUNTS"
    _cross_center_drive_time_key = "CROSS_CENTER_DRIVE_TIME"

    _robot = None
    _config = None
    _default_timeout = 15

    _starting_position = None

    _approach_speed = None
    _approach_encoder_counts = None
    _approach_encoder_threshold = None
    _approach_time = None
    _initial_wait_time = None

    _cross_encoder_threshold = None
    _cross_angle_threshold = None
    _cross_speed = None
    _cross_encoder_counts = None
    _cross_time = None
    _cross_center_turn_speed = None
    _cross_center_turn_angle = None
    _cross_center_turn_time = None
    _cross_center_drive_speed = None
    _cross_center_drive_encoder_counts = None
    _cross_center_drive_time = None

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
        self._add_cross_line_commands(self._robot.drivetrain.is_encoder_enabled(),
                                      self._robot.drivetrain.is_gyro_enabled())

        # abort all commands as the last command
        self.addSequential(Abort(self._robot))

    def _init_commands(self):
        self._approach_speed = self._config.getfloat(AutonomousCrossLine._approach_section,
                                                     AutonomousCrossLine._approach_speed_key)
        self._approach_encoder_counts = self._config.getint(AutonomousCrossLine._approach_section,
                                                            AutonomousCrossLine._approach_encoder_counts_key)
        self._approach_encoder_threshold = self._config.getint(AutonomousCrossLine._approach_section,
                                                               AutonomousCrossLine._approach_encoder_threshold_key)
        self._approach_time = self._config.getfloat(AutonomousCrossLine._approach_section,
                                                    AutonomousCrossLine._approach_time_key)
        self._initial_wait_time = self._config.getfloat(AutonomousCrossLine._approach_section,
                                                        AutonomousCrossLine._initial_wait_time_key)

        self._cross_encoder_threshold = self._config.getint(AutonomousCrossLine._cross_section,
                                                            AutonomousCrossLine._cross_encoder_threshold_key)
        self._cross_angle_threshold = self._config.getfloat(AutonomousCrossLine._cross_section,
                                                            AutonomousCrossLine._cross_angle_threshold_key)
        self._cross_speed = self._config.getfloat(AutonomousCrossLine._cross_section,
                                                  AutonomousCrossLine._cross_speed_key)
        self._cross_encoder_counts = self._config.getint(AutonomousCrossLine._cross_section,
                                                         AutonomousCrossLine._cross_encoder_counts_key)
        self._cross_time = self._config.getfloat(AutonomousCrossLine._cross_section,
                                                 AutonomousCrossLine._cross_time_key)
        self._cross_center_turn_speed = self._config.getfloat(AutonomousCrossLine._cross_section,
                                                              AutonomousCrossLine._cross_center_turn_speed_key)
        self._cross_center_turn_angle = self._config.getfloat(AutonomousCrossLine._cross_section,
                                                              AutonomousCrossLine._cross_center_turn_angle_key)
        self._cross_center_turn_time = self._config.getfloat(AutonomousCrossLine._cross_section,
                                                             AutonomousCrossLine._cross_center_turn_time_key)
        self._cross_center_drive_speed = self._config.getfloat(AutonomousCrossLine._cross_section,
                                                               AutonomousCrossLine._cross_center_drive_speed_key)
        self._cross_center_drive_encoder_counts = self._config.getint(
            AutonomousCrossLine._cross_section, AutonomousCrossLine._cross_center_drive_encoder_counts_key)
        self._cross_center_drive_time = self._config.getfloat(AutonomousCrossLine._cross_section,
                                                              AutonomousCrossLine._cross_center_drive_time_key)

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

    def _add_cross_line_commands(self, use_encoder=False, use_gyro=False):
        cross_line_commands = CommandGroup()
        # If starting in the center, avoid the tower
        if self._starting_position == 2:
            # Turn to avoid the tower
            if use_gyro:
                cross_line_commands.addSequential(TurnDegrees(self._robot, self._cross_center_turn_angle,
                                                              self._cross_center_turn_speed,
                                                              self._cross_angle_threshold),
                                                  self._default_timeout)
            else:
                cross_line_commands.addSequential(TurnTime(self._robot, self._cross_center_turn_time,
                                                           self._cross_center_turn_speed),
                                                  self._default_timeout)
            # Drive around the tower
            if use_encoder:
                cross_line_commands.addSequential(DriveEncoderCounts(self._robot,
                                                                     self._cross_center_drive_encoder_counts,
                                                                     self._cross_center_drive_speed,
                                                                     self._approach_encoder_threshold),
                                                  self._default_timeout)
            else:
                cross_line_commands.addSequential(DriveTime(self._robot, self._cross_center_drive_time,
                                                            self._cross_center_drive_speed),
                                                  self._default_timeout)
            # Turn back to facing forward
            if use_gyro:
                cross_line_commands.addSequential(TurnDegrees(self._robot, self._cross_center_turn_angle * -1.0,
                                                              self._cross_center_turn_speed,
                                                              self._cross_angle_threshold),
                                                  self._default_timeout)
            else:
                cross_line_commands.addSequential(TurnTime(self._robot, self._cross_center_turn_time,
                                                           self._cross_center_turn_speed * -1.0),
                                                  self._default_timeout)
        # Drive across the line
        if use_encoder:
            cross_line_commands.addSequential(DriveEncoderCounts(self._robot, self._cross_encoder_counts,
                                                                 self._cross_speed,
                                                                 self._cross_encoder_threshold),
                                              self._default_timeout)
        else:
            cross_line_commands.addSequential(DriveTime(self._robot, self._cross_time, self._cross_speed),
                                              self._default_timeout)

        self.addSequential(cross_line_commands)

    def initialize(self):
        pass  # Can be overwritten by teams

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
