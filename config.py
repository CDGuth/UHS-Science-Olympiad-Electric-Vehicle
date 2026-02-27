"""
Configuration file for the Science Olympiad Electric Vehicle 2026.
Contains physical constants, port assignments, control gains, and validation helpers.
!!!Runtime-editable run configuration now lives in user_input.py!!!
"""

from pybricks.parameters import Port, Direction, Color # pyright: ignore[reportMissingImports]
import math
import log_utils

# RUN MODES

MODE_STRAIGHT = "STRAIGHT"
MODE_BONUS = "BONUS"

# Constants
MM_PER_METER = 1000.0
MS_PER_SECOND = 1000.0


# ROBOT PHYSICAL CONSTANTS

# Steering Configuration
STEER_FRONT = "FRONT"
STEER_DIFF = "DIFFERENTIAL"
STEERING_TYPE = STEER_DIFF  # Set to STEER_DIFF to use differential steering
# Limits for FRONT steering
MAX_STEER_ANGLE = 45  # Degrees left/right from center
# Wheel specifications in millimeters
WHEEL_DIAMETER_MM = 56  # adjust as needed
WHEEL_CIRCUMFERENCE_MM = WHEEL_DIAMETER_MM * math.pi

# Track Width (for differential steering)
# Physical distance between the centers of the two drive wheels.
# Note: For skid steering or high-friction turns, the effective track width
# may be larger than the physical width due to wheel slip.
PHYSICAL_TRACK_WIDTH_MM = 150.0 
TRACK_WIDTH_SCALE = 1  # Scale factor for effective track width (1.0 = physical, >1.0 for skid)
EFFECTIVE_TRACK_WIDTH_MM = PHYSICAL_TRACK_WIDTH_MM * TRACK_WIDTH_SCALE

# IMPORTANT: Gear ratio (although this is techinically incorrect) is defined as Wheel Rotations / Motor Rotations.
# >1 means wheel turns faster than motor (speed increase).
# Example: If motor has 8 teeth and wheel gear has 16 teeth, ratio is 0.5.
# If motor has 16 teeth and wheel gear has 8 teeth, ratio is 2.0.
GEAR_RATIO = 3

# Distance per motor degree for odometry.
MM_PER_MOTOR_DEGREE = (WHEEL_CIRCUMFERENCE_MM / 360.0) * GEAR_RATIO

# Direction inverts
INVERT_DRIVE = True
INVERT_STEERING = False

# Can geometry (meters)
CAN_DIAMETER_M = 0.075  # rules: 7.0 to 8.0 cm
OUTER_CAN_INSIDE_EDGE_M = 1.0

# Calibration offsets
DISTANCE_CORRECTION_M = 0.00  # Added to the requested target distance to correct systematic bias

# Path Following
LOOKAHEAD_DIST_MM = 10.0
TARGET_REACHED_TOLERANCE_MM = 20.0



# PORT ASSIGNMENTS

PORT_STEER_MOTOR = None
PORT_LEFT_MOTOR = Port.A
PORT_RIGHT_MOTOR = Port.D
PORT_GYRO_SENSOR = Port.S4


# PID GAINS

# Front Steering PID
PID_HEADING_KP = 7.0
PID_HEADING_KI = 0.5
PID_HEADING_KD = 0.1
PID_FRONT_INTEGRAL_WINDOW_SIZE = 50  # Number of samples for front steering sliding-window integral

# Differential Steering PID
# Input: Heading Error (deg) -> Output: Turn Rate (deg/s) or Differential Speed
# Needs tuning separate from Front Steering.
PID_DIFF_HEADING_KP = 0.3
PID_DIFF_HEADING_KI = 0.004
PID_DIFF_HEADING_KD = 0.2
PID_DIFF_INTEGRAL_WINDOW_SIZE = 10  # Differential steering has its own sliding-window integral
PID_DIFF_INTEGRAL_ABS_MAX = 120.0  # Clamp integral state to reduce windup

# Motion constraints

MAX_SPEED_MM_S = 1200.0
MAX_ACCEL_MM_S2 = 800.0
MAX_DECEL_MM_S2 = 1400.0
MAX_DIFF_SPEED_MM_S = 100.0 # Max speed difference between motors for diff steering

# Logging
LOG_INTERVAL_MS = 50

# Gyro calibration
GYRO_CAL_DURATION_MS = 5000
GYRO_RESET_WAIT_MS = 100
GYRO_CAL_LOOP_WAIT_MS = 20
GYRO_CAL_SAMPLE_TIME_S = 0.02
GYRO_CAL_BLINK_INTERVAL_MS = 150

# UI Settings
UI_BLINK_INTERVAL_MS = 500
UI_PROGRESS_UPDATE_INTERVAL_MS = 150
UI_SUMMARY_WAIT_MS = 20

# Run Settings
RUN_START_DELAY_MS = 200
RUN_LOOP_WAIT_MS = 10
RUN_TIMEOUT_MULTIPLIER = 2.0
STALL_THRESHOLD_MM = 5.0
STALL_WINDOW_MS = 1200

# Strategy Settings
BONUS_PATH_INTEGRATION_STEPS = 50

# Input Settings
DISTANCE_STEP_REGIONAL_M = 0.25
DISTANCE_STEP_STATE_M = 0.10
DISTANCE_STEP_NATIONAL_M = 0.01
TIME_STEP_S = 0.50

# Battery checks
BATTERY_CHECK_ENABLED = True
MIN_BATTERY_VOLTAGE_V = 7.0

# Hardware precheck
HARDWARE_PRECHECK_ENABLED = True

# EVENT BOUNDS (for user input validation)
VALIDATION_ENABLED = True
MIN_TARGET_DISTANCE_M = 7.0
MAX_TARGET_DISTANCE_M = 10.0
MIN_TARGET_TIME_S = 10.0
MAX_TARGET_TIME_S = 20.0


# UTILITIES

def validate_config(config_dict):
    """
    Validates the user configuration against event rules.
    Returns (errors, warnings) where errors are dicts with message, key, and fixable.
    """
    if not VALIDATION_ENABLED:
        log_utils.log("Warning: Input validation is disabled.")
        return [], []
    errors = []
    warnings = []
    d = config_dict["target_distance_m"]
    t = config_dict["target_time_s"]
    gap = config_dict.get("bonus_gap_m", 0.0)

    if not (MIN_TARGET_DISTANCE_M <= d <= MAX_TARGET_DISTANCE_M):
        errors.append({"message": "Distance must be within event bounds (7.0-10.0 m).", "key": "target_distance_m", "fixable": True})

    if not (MIN_TARGET_TIME_S <= t <= MAX_TARGET_TIME_S):
        errors.append({"message": "Time must be within event bounds (10.0-20.0 s).", "key": "target_time_s", "fixable": True})

    if gap < 0.0 or gap > 1.0:
        errors.append({"message": "Bonus gap must be between 0.0 m and 1.0 m (can spacing).", "key": "bonus_gap_m", "fixable": True})

    if MAX_ACCEL_MM_S2 <= 0 or MAX_DECEL_MM_S2 <= 0 or MAX_SPEED_MM_S <= 0:
        errors.append({"message": "Speed and acceleration limits must be positive.", "key": None, "fixable": False})

    if errors:
        log_utils.log("Configuration errors:")
        for err in errors:
            log_utils.log(err["message"])
    else:
        log_utils.log("Configuration validated")

    return errors, warnings
