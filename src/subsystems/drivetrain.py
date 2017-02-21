import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.robotdrive import RobotDrive
from wpilib.victorsp import VictorSP
from wpilib.adxrs450_gyro import ADXRS450_Gyro
from wpilib.smartdashboard import SmartDashboard
from commands.tank_drive import TankDrive


class Drivetrain(Subsystem):
    # Config file section names
    _general_section = "DrivetrainGeneral"
    _left_motor_section = "DrivetrainLeftMotor"
    _right_motor_section = "DrivetrainRightMotor"
    _left_encoder_section = "DrivetrainLeftEncoder"
    _right_encoder_section = "DrivetrainRightEncoder"
    _gyro_section = "DrivetrainGyro"
    _enabled_key = "ENABLED"
    _a_channel_key = "A_CHANNEL"
    _b_channel_key = "B_CHANNEL"
    _inverted_key = "INVERTED"
    _type_key = "TYPE"
    _channel_key = "CHANNEL"
    _reversed_key = "REVERSED"

    _max_speed = 0

    _robot = None
    _config = None

    _left_motor = None
    _right_motor = None
    _robot_drive = None

    _left_encoder = None
    _left_encoder_a_channel = None
    _left_encoder_b_channel = None
    _left_encoder_reversed = None
    _left_encoder_type = None
    _left_encoder_count = 0

    _right_encoder = None
    _right_encoder_a_channel = None
    _right_encoder_b_channel = None
    _right_encoder_reversed = None
    _right_encoder_type = None
    _right_encoder_count = 0

    _gyro = None
    _gyro_angle = 0.0

    def __init__(self, robot, name=None, configfile='/home/lvuser/py/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard_sensors()
        self._update_smartdashboard_tank_drive(0.0, 0.0)
        self._update_smartdashboard_arcade_drive(0.0, 0.0)
        super().__init__(name=name)

    def initDefaultCommand(self):
        self.setDefaultCommand(TankDrive(self._robot, self._robot.oi))

    def get_left_encoder_value(self):
        if self._left_encoder:
            self._left_encoder_count = self._left_encoder.get()
        return self._left_encoder_count

    def get_right_encoder_value(self):
        if self._right_encoder:
            self._right_encoder_count = self._right_encoder.get()
        return self._right_encoder_count

    def get_encoder_value(self):
        if self._left_encoder and self._right_encoder:
            left_value = self.get_left_encoder_value()
            right_value = self.get_right_encoder_value()
            return int(round((left_value + right_value) / 2))
        elif self._left_encoder:
            return self.get_left_encoder_value()
        elif self._right_encoder:
            return self.get_right_encoder_value()
        else:
            return 0

    def reset_left_encoder_value(self):
        if self._left_encoder:
            self._left_encoder_count = 0
        self._update_smartdashboard_sensors()
        return self._left_encoder_count

    def reset_right_encoder_value(self):
        if self._right_encoder:
            self._right_encoder_count = 0
        self._update_smartdashboard_sensors()
        return self._right_encoder_count

    def reset_encoder_value(self):
        self.reset_left_encoder_value()
        self.reset_right_encoder_value()

    def get_gyro_angle(self):
        if self._gyro:
            self._gyro_angle = self._gyro.getAngle()
        return self._gyro_angle

    def reset_gyro_angle(self):
        if self._gyro:
            self._gyro.reset()
            self._gyro_angle = self._gyro.getAngle()
        self._update_smartdashboard_sensors()
        return self._gyro_angle

    def is_encoder_enabled(self):
        return self._left_encoder is not None or self._right_encoder is not None

    def is_gyro_enabled(self):
        return self._gyro is not None

    def tank_drive(self, left_speed, right_speed):
        left = left_speed * self._max_speed
        right = right_speed * self._max_speed
        self._robot_drive.tankDrive(left, right, False)
        self._update_smartdashboard_tank_drive(left_speed, right_speed)
        self.get_gyro_angle()
        self.get_left_encoder_value()
        self.get_right_encoder_value()
        self._update_smartdashboard_sensors()

    def arcade_drive(self, linear_distance, turn_angle, squared_inputs=True):
        if self._robot_drive:
            self._robot_drive.arcadeDrive(linear_distance, turn_angle, squared_inputs)
        self._update_smartdashboard_arcade_drive(linear_distance, turn_angle)
        self.get_gyro_angle()
        self.get_left_encoder_value()
        self.get_right_encoder_value()
        self._update_smartdashboard_sensors()

    def _update_smartdashboard_tank_drive(self, left, right):
        SmartDashboard.putNumber("Drivetrain Left Speed", left)
        SmartDashboard.putNumber("Drivetrain Right Speed", right)

    def _update_smartdashboard_arcade_drive(self, linear, turn):
        SmartDashboard.putNumber("Drivetrain Linear Speed", linear)
        SmartDashboard.putNumber("Drivetrain Turn Speed", turn)

    def _update_smartdashboard_sensors(self):
        SmartDashboard.putNumber("Drivetrain Left Encoder", self._left_encoder_count)
        SmartDashboard.putNumber("Drivetrain Right Encoder", self._right_encoder_count)
        SmartDashboard.putNumber("Gyro Angle", self._gyro_angle)

    def _init_components(self):
        self._max_speed = self._config.getfloat(self._general_section, "MAX_SPEED")

        if self._config.getboolean(Drivetrain._left_encoder_section, Drivetrain._enabled_key):
            self._left_encoder_a_channel = self._config.getint(self._left_encoder_section, Drivetrain._a_channel_key)
            self._left_encoder_b_channel = self._config.getint(self._left_encoder_section, Drivetrain._b_channel_key)
            self._left_encoder_reversed = self._config.getboolean(self._left_encoder_section, Drivetrain._reversed_key)
            self._left_encoder_type = self._config.getint(self._left_encoder_section, Drivetrain._type_key)
            if self._left_encoder_a_channel and self._left_encoder_b_channel and self._left_encoder_type:
                self._left_encoder = Encoder(self._left_encoder_a_channel, self._left_encoder_b_channel,
                                        self._left_encoder_reversed, self._left_encoder_type)

        if self._config.getboolean(Drivetrain._right_encoder_section, Drivetrain._enabled_key):
            self._right_encoder_a_channel = self._config.getint(self._right_encoder_section, Drivetrain._a_channel_key)
            self._right_encoder_b_channel = self._config.getint(self._right_encoder_section, Drivetrain._b_channel_key)
            self._right_encoder_reversed = self._config.getboolean(self._right_encoder_section, Drivetrain._reversed_key)
            self._right_encoder_type = self._config.getint(self._right_encoder_section, Drivetrain._type_key)
            if self._right_encoder_a_channel and self._right_encoder_b_channel and self._right_encoder_type:
                self._right_encoder = Encoder(self._right_encoder_a_channel, self._right_encoder_b_channel,
                                        self._right_encoder_reversed, self._right_encoder_type)

        if self._config.getboolean(Drivetrain._gyro_section, Drivetrain._enabled_key):
            gyro_channel = self._config.getint(self._gyro_section, Drivetrain._channel_key)
            self._gyro = ADXRS450_Gyro(gyro_channel)

        if self._config.getboolean(Drivetrain._left_motor_section, Drivetrain._enabled_key):
            self._left_motor = VictorSP(self._config.getint(self._left_motor_section, Drivetrain._channel_key))

        if self._config.getboolean(Drivetrain._right_motor_section, Drivetrain._enabled_key):
            self._right_motor = VictorSP(self._config.getint(self._right_motor_section, Drivetrain._channel_key))

        if self._left_motor and self._right_motor:
            self._robot_drive = RobotDrive(self._left_motor, self._right_motor)
            self._robot_drive.setSafetyEnabled(False)
            self._robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearLeft,
                                               self._config.getboolean(Drivetrain._left_motor_section,
                                                                       Drivetrain._inverted_key))
            self._robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearRight,
                                               self._config.getboolean(Drivetrain._right_motor_section,
                                                                       Drivetrain._inverted_key))
