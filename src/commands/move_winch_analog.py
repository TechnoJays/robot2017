from wpilib.command.command import Command
from oi import UserController, JoystickAxis


class MoveWinchAnalog(Command):
    JOYSTICK_LINEAR_SPEED = 1.0

    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.winch)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        move_speed = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.RIGHTY)
        self.robot.winch.move_winch(move_speed * self.JOYSTICK_LINEAR_SPEED)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.winch.move_winch(0)
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
