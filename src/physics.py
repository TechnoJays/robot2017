from pyfrc.physics import drivetrains


class PhysicsEngine(object):

    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        """
        
        self.physics_controller = physics_controller
        
        self.physics_controller.add_analog_gyro_channel(1)
            
    def update_sim(self, hal_data, now, tm_diff):
        """
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """

        """
        hal_data['pwm'] looks like this:
        [{
            'zero_latch': False,
            'initialized': False,
            'raw_value': 0,
            'value': 0,
            'period_scale': None,
            'type': None
        }, {
            'zero_latch': True,
            'initialized': True,
            'raw_value': 1011,
            'value': 0.0,
            'period_scale': 0,
            'type': 'talon'
        },...]
        """

        # Simulate the drivetrain
        l_motor = hal_data['pwm'][5]['value']
        r_motor = hal_data['pwm'][4]['value']
        
        speed, rotation = drivetrains.two_motor_drivetrain(l_motor, r_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)
