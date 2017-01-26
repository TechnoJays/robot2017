'''
Created on Jan 23, 2016

@author: Ty Strayer
'''

import configparser
import os

from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.robotdrive import RobotDrive
from wpilib.talon import Talon
from wpilib.analoggyro import AnalogGyro
from wpilib.smartdashboard import SmartDashboard

from commands.tank_drive import TankDrive


class Drivetrain(Subsystem):
    '''
    classdocs
    '''
    # 2 Talon controllers
    #

    # Config file section names
    left_motor_section = "DrivetrainLeftMotor"
    right_motor_section = "DrivetrainRightMotor"
    general_section = "DrivetrainGeneral"
    encoder_section = "DrivetrainEncoder"
    gyro_section = "DrivetrainGyro"
    pitch_gyro_section = "DrivetrainPitchGyro"

    # General config parameters
    _max_pickup_speed = 0

    _robot = None
    _config = None

    left_motor = None
    right_motor = None
    _robot_drive = None

    _encoder = None
    _encoder_a_channel = None
    _encoder_b_channel = None
    _encoder_reversed = None
    _encoder_type = None
    _encoder_count = 0

    _gyro = None
    _gyro_angle = 0.0

    _pitch_gyro = None
    _pitch_gyro_angle = 0.0

    def __init__(self, robot, name = None, configfile = '/home/lvuser/configs/subsystems.ini'):
        self._robot = robot;
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._load_general_config()
        self._init_components()
        self._update_smartdashboard_sensors()
        self._update_smartdashboard_tank_drive(0.0, 0.0)
        self._update_smartdashboard_arcade_drive(0.0, 0.0)
        super().__init__(name = name)

    def initDefaultCommand(self):
        self.setDefaultCommand(TankDrive(self._robot, self._robot.oi))

    def tankDrive(self, leftSpeed, rightSpeed):
        left = leftSpeed * self._max_pickup_speed
        right = rightSpeed * self._max_pickup_speed
        self._robot_drive.tankDrive(left, right, False)
        self._update_smartdashboard_tank_drive(leftSpeed, rightSpeed)
        self.get_gyro_angle()
        self.get_pitch_angle()
        self.get_encoder_value()
        self._update_smartdashboard_sensors()

    def _update_smartdashboard_tank_drive(self, left, right):
        SmartDashboard.putNumber("Drivetrain Left Speed", left)
        SmartDashboard.putNumber("Drivetrain Right Speed", right)

    def _load_general_config(self):
        self._max_pickup_speed = self._config.getfloat(self.general_section, "MAX_SPEED")

    def get_encoder_value(self):
        if(self._encoder):
            self._encoder_count = self._encoder.get()
        return self._encoder_count

    def reset_encoder_value(self):
        if(self._encoder):
            self._encoder_count = 0
        self._update_smartdashboard_sensors()
        return self._encoder_count

    def get_gyro_angle(self):
        if (self._gyro):
            self._gyro_angle = self._gyro.getAngle()
        return self._gyro_angle

    def reset_gyro_angle(self):
        if (self._gyro):
            self._gyro.reset()
            self._gyro_angle = self._gyro.getAngle()
        self._update_smartdashboard_sensors()
        return self._gyro_angle

    def get_pitch_angle(self):
        if (self._pitch_gyro):
            self._pitch_gyro_angle = self._pitch_gyro.getAngle()
        return self._pitch_gyro_angle

    def reset_pitch_angle(self):
        if (self._pitch_gyro):
            self._pitch_gyro.reset()
            self._pitch_gyro_angle = self._pitch_gyro.getAngle()
        self._update_smartdashboard_sensors()
        return self._pitch_gyro_angle

    def arcade_drive(self, linearDistance, turnAngle):
        if(self._robot_drive):
            self._robot_drive.arcadeDrive(linearDistance, turnAngle)
        self._update_smartdashboard_arcade_drive(linearDistance, turnAngle)
        self.get_gyro_angle()
        self.get_pitch_angle()
        self.get_encoder_value()
        self._update_smartdashboard_sensors()

    def _update_smartdashboard_arcade_drive(self, linear, turn):
        SmartDashboard.putNumber("Drivetrain Linear Speed", linear)
        SmartDashboard.putNumber("Drivetrain Turn Speed", turn)

    def _update_smartdashboard_sensors(self):
        SmartDashboard.putNumber("Drivetrain Encoder", self._encoder_count)
        SmartDashboard.putNumber("Gyro Angle", self._gyro_angle)
        SmartDashboard.putNumber("Pitch Angle", self._pitch_gyro_angle)

    def _init_components(self):
        if(self._config.getboolean(Drivetrain.encoder_section, "ENCODER_ENABLED")):
            self._encoder_a_channel = self._config.getint(self.encoder_section, "ENCODER_A_CHANNEL")
            self._encoder_b_channel = self._config.getint(self.encoder_section, "ENCODER_B_CHANNEL")
            self._encoder_reversed = self._config.getboolean(self.encoder_section, "ENCODER_REVERSED")
            self._encoder_type = self._config.getint(self.encoder_section, "ENCODER_TYPE")
            if(self._encoder_a_channel and self._encoder_b_channel and self._encoder_type):
                self._encoder = Encoder(self._encoder_a_channel, self._encoder_b_channel, self._encoder_reversed, self._encoder_type)

        if(self._config.getboolean(Drivetrain.gyro_section, "GYRO_ENABLED")):
            gyro_channel = self._config.getint(self.gyro_section, "GYRO_CHANNEL")
            gyro_sensitivity = self._config.getfloat(self.gyro_section, "GYRO_SENSITIVITY")
            if (gyro_channel):
                self._gyro = AnalogGyro(gyro_channel)
                if (self._gyro and gyro_sensitivity):
                    self._gyro.setSensitivity(gyro_sensitivity)

        if(self._config.getboolean(Drivetrain.pitch_gyro_section, "GYRO_ENABLED")):
            gyro_channel = self._config.getint(self.pitch_gyro_section, "GYRO_CHANNEL")
            gyro_sensitivity = self._config.getfloat(self.pitch_gyro_section, "GYRO_SENSITIVITY")
            if (gyro_channel):
                self._pitch_gyro = AnalogGyro(gyro_channel)
                if (self._pitch_gyro and gyro_sensitivity):
                    self._pitch_gyro.setSensitivity(gyro_sensitivity)

        if(self._config.getboolean(Drivetrain.left_motor_section, "MOTOR_ENABLED")):
            self.left_motor = Talon(self._config.getint(self.left_motor_section, "MOTOR_CHANNEL"))

        if(self._config.getboolean(Drivetrain.right_motor_section, "MOTOR_ENABLED")):
            self.right_motor = Talon(self._config.getint(self.right_motor_section, "MOTOR_CHANNEL"))

        if(self.left_motor and self.right_motor):
            self._robot_drive = RobotDrive(self.left_motor, self.right_motor)
            self._robot_drive.setSafetyEnabled(False)
            self._robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearLeft,
                                               self._config.getboolean(Drivetrain.left_motor_section,
                                                                       "MOTOR_INVERTED"))
            self._robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearRight,
                                               self._config.getboolean(Drivetrain.right_motor_section,
                                                                       "MOTOR_INVERTED"))
