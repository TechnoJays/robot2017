from wpilib.command.command import Command


class Abort(Command):
    _ran_once = False

    def __init__(self, robot, name=None, timeout=None):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.drivetrain)

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._ran_once = False

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.drivetrain.arcade_drive(0, 0)
        self._ran_once = True

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._ran_once or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
