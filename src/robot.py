from wpilib import command
import wpilib
from commands.do_nothing import DoNothing
from oi import OI
from subsystems.drivetrain import Drivetrain
from subsystems.winch import Winch
from subsystems.gear_feeder import GearFeeder
from commands.autonomous_cross_line import AutonomousCrossLine
from commands.autonomous_hang_center import AutonomousHangCenter


class MyRobot(wpilib.IterativeRobot):
    oi = None
    drivetrain = None
    winch = None
    autonomous_command = None
    gear_feeder = None

    def autonomousInit(self):
        # Schedule the autonomous command
        self.drivetrain.reset_gyro_angle()
        starting_position = self.oi.get_position()
        if self.oi.get_auto_choice() == 1:
            self.autonomous_command = AutonomousCrossLine(self)
            self.autonomous_command.set_match_configuration(starting_position)
        elif self.oi.get_auto_choice() == 2:
            self.autonomous_command = AutonomousHangCenter(self)
            self.autonomous_command.set_match_configuration(starting_position)
        else:
            self.autonomous_command = DoNothing(self)
        self.autonomous_command.start()

    def testInit(self):
        pass

    def teleopInit(self):
        if self.autonomous_command:
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
        self.winch = Winch(self)
        self.gear_feeder = GearFeeder(self)
        self.oi.setup_button_bindings()
        wpilib.CameraServer.launch()

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
