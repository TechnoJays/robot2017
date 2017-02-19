from wpilib.command.command import Command
import math


class DriveEncoderCounts(Command):
    _speed = None
    _encoder_threshold = None
    _encoder_change = None
    _target_position = None

    def __init__(self, robot, encoder_change, speed, threshold, name=None, timeout=15):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.drivetrain)
        self._encoder_change = encoder_change
        self._speed = speed
        self._encoder_threshold = threshold

    def initialize(self):
        """Called before the Command is run for the first time."""
        # Get initial position
        current = self.robot.drivetrain.get_encoder_value()
        # Calculate and store target
        self._target_position = current + self._encoder_change
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        # Get encoder count
        current = self.robot.drivetrain.get_encoder_value()
        distance_left = self._target_position - current
        # Determine direction using target and current encoder values
        if distance_left >= 0:
            direction = -1.0
        else:
            direction = 1.0
        linear_drive_amount = self._speed * direction
        # Set drivetrain using speed and direction
        self.robot.drivetrain.arcade_drive(linear_drive_amount, 0.0, False)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        # Get encoder count
        current = self.robot.drivetrain.get_encoder_value()
        # If abs(target - current) < threshold then return true
        return math.fabs(self._target_position - current) <= self._encoder_threshold or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        # Stop driving
        self.robot.drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
