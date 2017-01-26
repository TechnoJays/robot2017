from wpilib.command.command import Command
import math

class TurnDegrees(Command):
    '''
    classdocs
    '''
    _speed = None
    _degree_threshold = None
    _degrees_change = None
    _target_degrees = None

    def __init__(self, robot, degrees_change, speed, threshold, name=None, timeout=15):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        self.robot = robot;
        self.requires(robot.drivetrain)
        self._degrees_change = degrees_change
        self._speed = speed
        self._degree_threshold = threshold

    def initialize(self):
        """Called before the Command is run for the first time."""
        # Get initial position
        current = self.robot.drivetrain.get_gyro_angle()
        # Calculate and store target
        self._target_degrees = current + self._degrees_change
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        current = self.robot.drivetrain.get_gyro_angle()
        degrees_left = self._target_degrees - current
        if (degrees_left) >= 0:
            direction = 1.0
        else:
            direction = -1.0
        turn_speed = self._speed * direction
        # Set drivetrain using speed and direction
        self.robot.drivetrain.arcade_drive(0.0, turn_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        current = self.robot.drivetrain.get_gyro_angle()
        # If abs(target - current) < threshold then return true
        return math.fabs(self._target_degrees - current) <= self._degree_threshold or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        # Stop driving
        self.robot.drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
