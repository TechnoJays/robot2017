from wpilib import command
import wpilib

from commands.do_nothing import DoNothing
from oi import OI
from subsystems.drivetrain import Drivetrain


class MyRobot(wpilib.IterativeRobot):
    oi = None
    drivetrain = None

    def autonomousInit(self):
        #Schedule the autonomous command
        self.drivetrain.reset_gyro_angle()
        if self.oi.get_auto_choice() == 1:
            self.autonomous_command = DoNothing(self)
        else:
            self.autonomous_command = DoNothing(self)
        self.autonomous_command.start()

    def testInit(self):
        pass

    # Subsystems

    def teleopInit(self):
        self.autonomous_command.cancel()
        self.teleopInitialized = True

    def disabledInit(self):
        self.disabledInitialized = True

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.oi = OI(self)
        self.drivetrain = Drivetrain(self)

        self.oi.setup_button_bindings()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        command.Scheduler.getInstance().run()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        command.Scheduler.getInstance().run()

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
