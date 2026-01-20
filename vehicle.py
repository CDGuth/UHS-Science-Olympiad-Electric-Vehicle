"""Hardware abstraction layer for the EV3 vehicle."""

import math
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
        
        self.steer_type = config.STEERING_TYPE
        if self.steer_type == config.STEER_FRONT:
            self.steer_motor = Motor(config.PORT_STEER_MOTOR, steer_dir) # pyright: ignore
        else:
            self.steer_motor = None # Steering motor not needed in differential mode

        self.gyro = GyroSensor(config.PORT_GYRO_SENSOR)
        self.pid_timer = StopWatch(); self.pid_timer.reset()
        self.heading_timer = StopWatch(); self.heading_timer.reset()
        self.drift_rate_dps = 0.0

        # Odometry State
        self.distance_mm = 0.0
        self.start_angle_left = 0
        self.start_angle_right = 0
        
        self.target_speed_mm_s = 0.0 # Store speed for differential mixing

        self.pid_integral = 0
        self.pid_last_error = 0
        self.last_time = 0

        # Position tracking
        self.x_mm = 0.0
        self.y_mm = 0.0
        self.last_odo_dist = 0.0

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
        self.last_time = 0

        self.x_mm = 0.0
        self.y_mm = 0.0
        self.last_odo_dist = 0.0

    def update_sensors(self):
        l_angle = self.left_motor.angle()
        r_angle = self.right_motor.angle()
        avg_angle = (l_angle + r_angle) / 2.0
        
        current_dist = avg_angle * config.MM_PER_MOTOR_DEGREE
        delta_dist = current_dist - self.last_odo_dist
        self.distance_mm = current_dist
        self.last_odo_dist = current_dist

        # Update X, Y
        # Heading is in degrees, convert to radians
        # Coordinate system: X is forward, Y is Left.
        # Heading 0 is along +X. Positive heading is Left (+Y).
        heading_rad = math.radians(self.get_heading())
        self.x_mm += delta_dist * math.cos(heading_rad)
        self.y_mm += delta_dist * math.sin(heading_rad)
        
    def get_distance(self):
        return self.distance_mm
    
    def get_pose(self):
        """Returns tuple (x_mm, y_mm, heading_deg, distance_mm)"""
        return self.x_mm, self.y_mm, self.get_heading(), self.distance_mm
        
    def get_heading(self):
        elapsed_s = self.heading_timer.time() / config.MS_PER_SECOND
        return self.gyro.angle() - self.drift_rate_dps * elapsed_s

    def drive_speed(self, speed_mm_s):
        self.target_speed_mm_s = speed_mm_s
        
        if self.steer_type == config.STEER_FRONT:
            motor_speed_deg_s = speed_mm_s / config.MM_PER_MOTOR_DEGREE
            self.left_motor.run(motor_speed_deg_s)
            self.right_motor.run(motor_speed_deg_s)
        # For DIFF Steering, we wait for steer_heading to apply the speed+turn mix

    def steer_heading(self, target_heading):
        current_heading = self.get_heading()
        error = target_heading - current_heading
        
        current_time = self.pid_timer.time()
        dt = (current_time - self.last_time) / config.MS_PER_SECOND # seconds
        self.last_time = current_time
        
        if dt <= 0:
            return

        if self.steer_type == config.STEER_FRONT:
            kp = config.PID_HEADING_KP
            ki = config.PID_HEADING_KI
            kd = config.PID_HEADING_KD
        else:
            kp = config.PID_DIFF_HEADING_KP
            ki = config.PID_DIFF_HEADING_KI
            kd = config.PID_DIFF_HEADING_KD

        p_term = kp * error
        self.pid_integral += error * dt
        i_term = ki * self.pid_integral
        derivative = (error - self.pid_last_error) / dt
        d_term = kd * derivative
        
        self.pid_last_error = error
        
        pid_output = p_term + i_term + d_term
        
        if self.steer_type == config.STEER_FRONT:
            steer_angle_target = pid_output
            if steer_angle_target > config.MAX_STEER_ANGLE:
                steer_angle_target = config.MAX_STEER_ANGLE
            elif steer_angle_target < -config.MAX_STEER_ANGLE:
                steer_angle_target = -config.MAX_STEER_ANGLE

            if self.steer_motor:
                self.steer_motor.track_target(steer_angle_target)
            
        elif self.steer_type == config.STEER_DIFF:
            # PID output is interpreted as differential speed adjustment (turn rate control)
            # v_l = v - adjustment
            # v_r = v + adjustment
            
            # Use degrees/s directly for easier tuning relative to gyro:
            omega_deg_s = pid_output
            
            # Apply steering inversion if requested
            if config.INVERT_STEERING:
                omega_deg_s = -omega_deg_s

            omega_rad_s = math.radians(omega_deg_s)
            
            # v = r * omega.  v_diff = (width/2) * omega
            diff_mm_s = (config.EFFECTIVE_TRACK_WIDTH_MM / 2.0) * omega_rad_s
            
            # Clamp the max speed difference to avoid aggressive turns or wheel slip
            if diff_mm_s > config.MAX_DIFF_SPEED_MM_S:
                diff_mm_s = config.MAX_DIFF_SPEED_MM_S
            elif diff_mm_s < -config.MAX_DIFF_SPEED_MM_S:
                diff_mm_s = -config.MAX_DIFF_SPEED_MM_S

            # base_mm_s is the target forward speed
            base_mm_s = self.target_speed_mm_s
            
            # v_right > v_left turns the vehicle LEFT (positive heading)
            v_left_mm_s = base_mm_s - diff_mm_s
            v_right_mm_s = base_mm_s + diff_mm_s

            # Clamp speeds so they cannot be negative (prevent reversing during steering)
            v_left_mm_s = max(0, v_left_mm_s)
            v_right_mm_s = max(0, v_right_mm_s)
            
            # Convert to motor degrees/s
            speed_l_deg_s = v_left_mm_s / config.MM_PER_MOTOR_DEGREE
            speed_r_deg_s = v_right_mm_s / config.MM_PER_MOTOR_DEGREE
            
            self.left_motor.run(speed_l_deg_s)
            self.right_motor.run(speed_r_deg_s)


    def stop(self, brake=True):
        if brake:
            self.left_motor.hold()
            self.right_motor.hold()
            if self.steer_motor:
                self.steer_motor.track_target(0)
                self.steer_motor.hold()
        else:
            self.left_motor.stop()
            self.right_motor.stop()
            if self.steer_motor:
                self.steer_motor.track_target(0)
                self.steer_motor.stop()

    def calibrate_gyro_drift(self, duration_ms=None, progress_cb=None):
        """Calibrates gyro drift; safe to call multiple times."""
        cal_ms = duration_ms if duration_ms is not None else config.GYRO_CAL_DURATION_MS
        log_utils.log("Starting gyro calibration for {:.1f} s. Do not move the vehicle.".format(cal_ms / config.MS_PER_SECOND))
        self.ev3.light.off()
        blink_timer = StopWatch(); blink_timer.reset()
        self.gyro.reset_angle(0)
        wait(config.GYRO_RESET_WAIT_MS)

        timer = StopWatch(); timer.reset()
        last_angle = self.gyro.angle()
        drift_sum = 0.0
        samples = 0

        while timer.time() < cal_ms:
            if (blink_timer.time() // config.GYRO_CAL_BLINK_INTERVAL_MS) % 2 == 0:
                self.ev3.light.on(config.Color.YELLOW)
            else:
                self.ev3.light.off()

            wait(config.GYRO_CAL_LOOP_WAIT_MS)
            angle = self.gyro.angle()
            drift_sum += (angle - last_angle) / config.GYRO_CAL_SAMPLE_TIME_S
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
