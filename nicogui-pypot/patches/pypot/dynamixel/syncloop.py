from ..robot.controller import MotorsController
from .controller import (
    AngleLimitRegisterController,
    DxlController,
    PosSpeedLoadDxlController,
)


class MetaDxlController(MotorsController):
    """ Synchronizes the reading/writing of :class:`~pypot.dynamixel.motor.DxlMotor` with the real motors.

        This class handles synchronization loops that automatically read/write values from the "software" :class:`~pypot.dynamixel.motor.DxlMotor` with their "hardware" equivalent. Those loops shared a same :class:`~pypot.dynamixel.io.DxlIO` connection to avoid collision in the bus. Each loop run within its own thread as its own frequency.

        .. warning:: As all the loop attached to a controller shared the same bus, you should make sure that they can run without slowing down the other ones.

        """

    def __init__(self, io, motors, controllers):
        MotorsController.__init__(self, io, motors, 1.0)
        self.controllers = controllers

    def setup(self):
        """ Starts all the synchronization loops. """
        [c.start() for c in self.controllers]
        [c.wait_to_start() for c in self.controllers]

    def update(self):
        pass

    def teardown(self):
        """ Stops the synchronization loops. """
        [c.stop() for c in self.controllers]


class BaseDxlController(MetaDxlController):
    """ Implements a basic controller that synchronized the most frequently used values.

    More precisely, this controller:
        * reads the present position, speed, load at 50Hz
        * writes the goal position, moving speed and torque limit at 50Hz
        * writes the pid gains (or compliance margin and slope) at 10Hz
        * reads the present voltage and temperature at 1Hz

    """

    def __init__(self, io, motors):
        controllers = [
            PosSpeedLoadDxlController(io, motors, 50.0),
            AngleLimitRegisterController(io, motors, 10.0, False),
            DxlController(io, motors, 1.0, False, "get", "present_voltage"),
            DxlController(io, motors, 1.0, False, "get", "present_temperature"),
        ]

        pid_motors = [
            m
            for m in motors
            if (m.model.startswith("MX") or m.model.startswith("XL-320"))
        ]
        if pid_motors:
            controllers.insert(
                0, DxlController(io, pid_motors, 10.0, False, "set", "pid_gain", "pid")
            )

        force_control_motors = [m for m in motors if m.model.startswith("SR-RH4D")]

        if force_control_motors:
            controllers.insert(
                0,
                DxlController(
                    io,
                    force_control_motors,
                    10.0,
                    False,
                    "set",
                    "force_control_enable",
                    "force_control_enable",
                ),
            )
            controllers.insert(
                0,
                DxlController(
                    io,
                    force_control_motors,
                    10.0,
                    False,
                    "set",
                    "goal_force",
                    "goal_force",
                ),
            )

        current_motors = [
            m
            for m in motors
            if (
                m.model.startswith("MX-64")
                or m.model.startswith("MX-106")
                or m.model.startswith("SR-RH4D")
            )
        ]

        if current_motors:
            controllers.insert(
                0,
                DxlController(
                    io,
                    current_motors,
                    10.0,
                    False,
                    "get",
                    "present_current",
                    "present_current",
                ),
            )

        seed_eros_motors = [m for m in motors if (m.model.startswith("SR-SEED"))]

        if seed_eros_motors:
            controllers.insert(
                0,
                DxlController(
                    io, seed_eros_motors, 1.0, False, "set", "pid_lock", "pid_lock"
                ),
            )
            controllers.insert(
                0,
                DxlController(
                    io, seed_eros_motors, 1.0, True, "set", "pid_gain", "pid"
                ),
            )

        seed_logic_boards = [m for m in motors if (m.model.startswith("SR-EROSBRD"))]

        if seed_logic_boards:
            controllers.insert(
                0,
                DxlController(
                    io,
                    seed_logic_boards,
                    10.0,
                    False,
                    "get",
                    "present_motor_currents",
                    "present_motor_currents",
                ),
            )
            if seed_logic_boards[0].__class__.__name__[-1] != '-':
                controllers.insert(
                    0,
                    DxlController(
                        io,
                        seed_logic_boards,
                        1.0,
                        False,
                        "set",
                        "attached_motor_ids",
                        "attached_motor_ids",
                    ),
                )
            controllers.insert(
                0,
                DxlController(
                    io,
                    seed_logic_boards,
                    10.0,
                    False,
                    "get",
                    "palm_sensor_reading",
                    "palm_sensor_reading",
                ),
            )
            controllers.insert(
                0,
                DxlController(
                    io,
                    seed_logic_boards,
                    1.0,
                    False,
                    "get",
                    "palm_sensor_installed",
                    "palm_sensor_installed",
                ),
            )

        margin_slope_motors = [
            m for m in motors if (m.model.startswith("AX") or m.model.startswith("RX"))
        ]
        if margin_slope_motors:
            controllers.append(
                DxlController(
                    io, margin_slope_motors, 10, False, "set", "compliance_margin"
                )
            )
            controllers.append(
                DxlController(
                    io, margin_slope_motors, 10, False, "set", "compliance_slope"
                )
            )

        MetaDxlController.__init__(self, io, motors, controllers)


class LightDxlController(MetaDxlController):
    def __init__(self, io, motors):
        controllers = [
            PosSpeedLoadDxlController(io, motors, 50.0),
            AngleLimitRegisterController(io, motors, 10.0, True),
            DxlController(io, motors, 10.0, True, "get", "present_voltage"),
            DxlController(io, motors, 10.0, True, "get", "present_temperature"),
        ]

        pid_motors = [
            m
            for m in motors
            if (m.model.startswith("MX") or m.model.startswith("XL-320"))
        ]
        if pid_motors:
            controllers.insert(
                0, DxlController(io, pid_motors, 10.0, True, "set", "pid_gain", "pid")
            )

        margin_slope_motors = [
            m for m in motors if (m.model.startswith("AX") or m.model.startswith("RX"))
        ]
        if margin_slope_motors:
            controllers.append(
                DxlController(
                    io, margin_slope_motors, 10.0, True, "set", "compliance_margin"
                )
            )
            controllers.append(
                DxlController(
                    io, margin_slope_motors, 10.0, True, "set", "compliance_slope"
                )
            )

        led_motors = [m for m in motors if m.model.startswith("XL-320")]
        if led_motors:
            controllers.append(
                DxlController(io, led_motors, 5.0, False, "set", "LED_color", "led")
            )

        MetaDxlController.__init__(self, io, motors, controllers)
