from wpilib.command.command import Command
from oi import UserController, JoystickButtons

class ReleaseGear(Command):

    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.gear_release)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.gear_release.set_gear_release(True)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.gear_release.set_gear_release(False)
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
