from wpilib.command.command import Command
from oi import JoystickAxis, UserController


class TankDrive(Command):

    def __init__(self, robot, name=None, stick_scaling=1, dpad_scaling=0.5, timeout=15):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.drivetrain)
        self._dpad_scaling = dpad_scaling
        self._stick_scaling = stick_scaling

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        dpad_y = self.robot.oi.get_axis(UserController.DRIVER, JoystickAxis.DPADY)
        if dpad_y != 0.0:
            self.robot.drivetrain.arcade_drive(self._dpad_scaling * dpad_y, 0.0)
        else:
            left_track = self.robot.oi.get_axis(UserController.DRIVER, JoystickAxis.LEFTY)
            right_track = self.robot.oi.get_axis(UserController.DRIVER, JoystickAxis.RIGHTY)
            self.robot.drivetrain.tank_drive(self._stick_scaling * left_track, self._stick_scaling * right_track)
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
