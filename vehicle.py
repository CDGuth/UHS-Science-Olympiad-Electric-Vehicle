"""Hardware abstraction layer for the EV3 vehicle."""

from pybricks.hubs import EV3Brick  # pyright: ignore[reportMissingImports]
from pybricks.ev3devices import Motor, GyroSensor  # pyright: ignore[reportMissingImports]
from pybricks.parameters import Port, Stop, Direction  # pyright: ignore[reportMissingImports]
from pybricks.tools import wait, StopWatch  # pyright: ignore[reportMissingImports]
import config
import log_utils


class Car:
    def __init__(self, auto_calibrate=False, ev3=None):
        self.ev3 = ev3 if ev3 is not None else EV3Brick()

        drive_dir = Direction.COUNTERCLOCKWISE if config.INVERT_DRIVE else Direction.CLOCKWISE
        steer_dir = Direction.COUNTERCLOCKWISE if config.INVERT_STEERING else Direction.CLOCKWISE

        self.left_motor = Motor(config.PORT_LEFT_MOTOR, drive_dir)
        self.right_motor = Motor(config.PORT_RIGHT_MOTOR, drive_dir)
        self.steer_motor = Motor(config.PORT_STEER_MOTOR, steer_dir)

        self.gyro = GyroSensor(config.PORT_GYRO_SENSOR)
        self.pid_timer = StopWatch(); self.pid_timer.reset()
        self.heading_timer = StopWatch(); self.heading_timer.reset()
        self.drift_rate_dps = 0.0

        # Odometry State
        self.distance_mm = 0.0
        self.start_angle_left = 0
        self.start_angle_right = 0

        self.pid_integral = 0
        self.pid_last_error = 0
        self.last_time = 0

        if auto_calibrate:
            self.calibrate_gyro_drift()

    def reset_odometry(self):
        """
        Resets distance and angle measurements to zero.
        Should be called just before the run starts.
        """
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)
        self.gyro.reset_angle(0)
        self.heading_timer.reset()
        
        self.distance_mm = 0.0
        self.pid_integral = 0
        self.pid_last_error = 0
        self.pid_timer.reset()

    def update_sensors(self):
        l_angle = self.left_motor.angle()
        r_angle = self.right_motor.angle()
        avg_angle = (l_angle + r_angle) / 2.0
        
        self.distance_mm = avg_angle * config.MM_PER_MOTOR_DEGREE
        
    def get_distance(self):
        return self.distance_mm
        
    def get_heading(self):
        elapsed_s = self.heading_timer.time() / 1000.0
        return self.gyro.angle() - self.drift_rate_dps * elapsed_s

    def drive_speed(self, speed_mm_s):
        motor_speed_deg_s = speed_mm_s / config.MM_PER_MOTOR_DEGREE
        self.left_motor.run(motor_speed_deg_s)
        self.right_motor.run(motor_speed_deg_s)

    def steer_heading(self, target_heading):
        current_heading = self.get_heading()
        error = target_heading - current_heading
        
        current_time = self.pid_timer.time()
        dt = (current_time - self.last_time) / 1000.0 # seconds
        self.last_time = current_time
        
        if dt <= 0:
            return

        p_term = config.PID_HEADING_KP * error
        self.pid_integral += error * dt
        i_term = config.PID_HEADING_KI * self.pid_integral
        derivative = (error - self.pid_last_error) / dt
        d_term = config.PID_HEADING_KD * derivative
        
        self.pid_last_error = error
        
        steer_angle_target = p_term + i_term + d_term
        
        if steer_angle_target > config.MAX_STEER_ANGLE:
            steer_angle_target = config.MAX_STEER_ANGLE
        elif steer_angle_target < -config.MAX_STEER_ANGLE:
            steer_angle_target = -config.MAX_STEER_ANGLE

        self.steer_motor.track_target(steer_angle_target)

    def stop(self, brake=True):
        mode = Stop.HOLD if brake else Stop.COAST
        self.left_motor.stop(mode)
        self.right_motor.stop(mode)
        self.steer_motor.track_target(0)
        self.steer_motor.stop(Stop.HOLD)

    def calibrate_gyro_drift(self, duration_ms=None, progress_cb=None):
        """Calibrates gyro drift; safe to call multiple times."""
        cal_ms = duration_ms if duration_ms is not None else config.GYRO_CAL_DURATION_MS
        log_utils.log("Starting gyro calibration for {:.1f} s. Do not move the vehicle.".format(cal_ms / 1000.0))
        self.ev3.light.off()
        blink_timer = StopWatch(); blink_timer.reset()
        self.gyro.reset_angle(0)
        wait(100)

        timer = StopWatch(); timer.reset()
        last_angle = self.gyro.angle()
        drift_sum = 0.0
        samples = 0

        while timer.time() < cal_ms:
            if (blink_timer.time() // 150) % 2 == 0:
                self.ev3.light.on(config.Color.YELLOW)
            else:
                self.ev3.light.off()

            wait(20)
            angle = self.gyro.angle()
            drift_sum += (angle - last_angle) / 0.02
            samples += 1
            last_angle = angle

            if progress_cb:
                progress_cb(timer.time() / cal_ms)

        self.ev3.light.off()
        self.drift_rate_dps = drift_sum / max(1, samples)
        if progress_cb:
            progress_cb(1.0)
        log_utils.log("Gyro calibration complete; drift={:.4f} deg/s".format(self.drift_rate_dps))
        self.heading_timer.reset()
        return self.drift_rate_dps
