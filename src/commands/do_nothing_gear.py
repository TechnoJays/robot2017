from wpilib.command.command import Command


class DoNothingGear(Command):

    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.gear_feeder)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
