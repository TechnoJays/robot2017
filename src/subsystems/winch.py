
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from commands.move_winch_analog import MoveWinchAnalog
from wpilib.smartdashboard import SmartDashboard

import configparser
import os
from wpilib.spark import Spark


class Winch(Subsystem):

    _motor_section = "WinchMotor"
    _encoder_section = "WinchEncoder"
    _enabled = "ENABLED"
    _channel = "CHANNEL"
    _inverted = "INVERTED"

    _robot = None
    _subsystem_config = None
    _motor = None
    _encoder = None
    _encoder_value = 0


    def __init__(self, robot, name=None, configfile = '../src/configs/subsystems.ini'):
        self._robot = robot
        self._subsystem_config = configfile
        self._init_components()
        self._update_smartdashboard(0.0)
        super().__init__(name = name)

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveWinchAnalog(self._robot))

    def move_winch(self, speed):
        if self._motor:
            self._motor.setSpeed(speed)
        self.get_encoder_value()
        self._update_smartdashboard(speed)

    def get_encoder_value(self):
        if self._encoder:
            self._encoder_value = self._encoder.get()
        return self._encoder_value

    def reset_encoder_value(self):
        if self._encoder:
            self._encoder.reset()
            self._encoder_value = self._encoder.get()
        self._update_smartdashboard(0.0)
        return self._encoder_value

    def _update_smartdashboard(self, speed):
        SmartDashboard.putNumber("Winch Encoder", self._encoder_value)
        SmartDashboard.putNumber("Winch Speed", speed)

    def _init_components(self):

        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), self._subsystem_config))

        if config.getboolean(self._motor_section, self._enabled):
            motor_channel = config.getint(self._motor_section, self._channel)
            motor_inverted = config.getboolean(self._motor_section , self._inverted)
            if motor_channel:
                self._motor = Spark(motor_channel)
                if self._motor:
                    self._motor.setInverted(motor_inverted)

        if config.getboolean(self._encoder_section, self._enabled):
            encoder_a_channel = config.getint(self._encoder_section, "A_CHANNEL")
            encoder_b_channel = config.getint(self._encoder_section, "B_CHANNEL")
            encoder_inverted = config.getboolean(self._encoder_section, self._inverted)
            encoder_type = config.getint(self._encoder_section, "TYPE")
            if encoder_a_channel and encoder_b_channel and encoder_type:
                self._encoder = Encoder(encoder_a_channel, encoder_b_channel, encoder_inverted, encoder_type)