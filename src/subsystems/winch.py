import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.smartdashboard import SmartDashboard
from wpilib.spark import Spark
from commands.move_winch import MoveWinch


class Winch(Subsystem):
    # Config file section names
    _motor_section = "WinchMotor"
    _encoder_section = "WinchEncoder"
    _enabled_key = "ENABLED"
    _a_channel_key = "A_CHANNEL"
    _b_channel_key = "B_CHANNEL"
    _inverted_key = "INVERTED"
    _type_key = "TYPE"
    _channel_key = "CHANNEL"
    _reversed_key = "REVERSED"

    _robot = None
    _config = None

    _motor = None
    _encoder = None
    _encoder_count = 0

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard(0.0)
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveWinch(self._robot))

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
        if self._config.getboolean(Winch._motor_section, Winch._enabled_key):
            motor_channel = self._config.getint(Winch._motor_section, Winch._channel_key)
            motor_inverted = self._config.getboolean(Winch._motor_section, Winch._inverted_key)
            self._motor = Spark(motor_channel)
            if self._motor:
                self._motor.setInverted(motor_inverted)

        if self._config.getboolean(Winch._encoder_section, Winch._enabled_key):
            encoder_a_channel = self._config.getint(Winch._encoder_section, Winch._a_channel_key)
            encoder_b_channel = self._config.getint(Winch._encoder_section, Winch._b_channel_key)
            encoder_inverted = self._config.getboolean(Winch._encoder_section, Winch._reversed_key)
            encoder_type = self._config.getint(Winch._encoder_section, Winch._type_key)
            self._encoder = Encoder(encoder_a_channel, encoder_b_channel, encoder_inverted, encoder_type)
