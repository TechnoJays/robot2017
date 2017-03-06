from wpilib.command.command import Command
from oi import JoystickAxis, UserController


class MoveWinch(Command):

    def __init__(self, robot, name=None, timeout=15):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.winch)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        right_stick = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.RIGHTY)
        if right_stick > 0.0:
            self.robot.winch.move_winch(right_stick)
        else:
            self.robot.winch.move_winch(0.0)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        pass
