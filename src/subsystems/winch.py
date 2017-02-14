import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from commands.move_winch_analog import MoveWinchAnalog
from wpilib.smartdashboard import SmartDashboard
from wpilib.spark import Spark


class Winch(Subsystem):
    # Config file section names
    _motor_section = "WinchMotor"
    _encoder_section = "WinchEncoder"

    _robot = None
    _config = None

    _motor = None
    _encoder = None
    _encoder_count = 0

    def __init__(self, robot, name=None, configfile='/home/lvuser/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard(0.0)
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveWinchAnalog(self._robot))

    def move_winch(self, speed):
        if self._motor:
            self._motor.setSpeed(speed)
        self.get_encoder_value()
        self._update_smartdashboard(speed)

    def get_encoder_value(self):
        if self._encoder:
            self._encoder_count = self._encoder.get()
        return self._encoder_count

    def reset_encoder_value(self):
        if self._encoder:
            self._encoder.reset()
            self._encoder_count = self._encoder.get()
        self._update_smartdashboard(0.0)
        return self._encoder_count

    def _update_smartdashboard(self, speed):
        SmartDashboard.putNumber("Winch Encoder", self._encoder_count)
        SmartDashboard.putNumber("Winch Speed", speed)

    def _init_components(self):
        if self._config.getboolean(Winch._motor_section, "MOTOR_ENABLED"):
            motor_channel = self._config.getint(Winch._motor_section, "MOTOR_CHANNEL")
            motor_inverted = self._config.getboolean(Winch._motor_section, "MOTOR_INVERTED")
            self._motor = Spark(motor_channel)
            if self._motor:
                self._motor.setInverted(motor_inverted)

        if self._config.getboolean(Winch._encoder_section, "ENCODER_ENABLED"):
            encoder_a_channel = self._config.getint(Winch._encoder_section, "ENCODER_A_CHANNEL")
            encoder_b_channel = self._config.getint(Winch._encoder_section, "ENCODER_B_CHANNEL")
            encoder_inverted = self._config.getboolean(Winch._encoder_section, "ENCODER_REVERSED")
            encoder_type = self._config.getint(Winch._encoder_section, "ENCODER_TYPE")
            self._encoder = Encoder(encoder_a_channel, encoder_b_channel, encoder_inverted, encoder_type)
