#!/usr/bin/env pybricks-micropython
"""Main execution entry point for the Science Olympiad Electric Vehicle 2026."""

from pybricks.hubs import EV3Brick  # pyright: ignore[reportMissingImports]
from pybricks.ev3devices import Motor, GyroSensor  # pyright: ignore[reportMissingImports]
from pybricks.parameters import Button  # pyright: ignore[reportMissingImports]
from pybricks.tools import wait, StopWatch  # pyright: ignore[reportMissingImports]

import config
import user_input
from vehicle import Car
from strategies import get_strategy
from run_logger import RunLogger
from ui.ui_flow import collect_run_config
from ui.run_status import show_progress
from ui.run_summary_screen import show_summary
from ui.common import show_warning
import log_utils


def _port_label(port):
    return str(port)


def precheck_devices(ev3):
    missing = []

    if config.BATTERY_CHECK_ENABLED:
        voltage_v = ev3.battery.voltage() / 1000.0
        if voltage_v < config.MIN_BATTERY_VOLTAGE_V:
            msg = "Battery too low: {:.2f} V (min {:.2f} V).".format(voltage_v, config.MIN_BATTERY_VOLTAGE_V)
            show_warning(ev3, "Battery Low", [msg])
            log_utils.log(msg)
            raise RuntimeError(msg)
        log_utils.log("Battery check passed: {:.2f} V.".format(voltage_v))

    def try_create(name, ctor):
        try:
            ctor()
        except Exception:
            missing.append(name)

    try_create("Left motor on {}".format(_port_label(config.PORT_LEFT_MOTOR)), lambda: Motor(config.PORT_LEFT_MOTOR))
    try_create("Right motor on {}".format(_port_label(config.PORT_RIGHT_MOTOR)), lambda: Motor(config.PORT_RIGHT_MOTOR))
    try_create("Steering motor on {}".format(_port_label(config.PORT_STEER_MOTOR)), lambda: Motor(config.PORT_STEER_MOTOR))
    try_create("Gyro on {}".format(_port_label(config.PORT_GYRO_SENSOR)), lambda: GyroSensor(config.PORT_GYRO_SENSOR))

    if missing:
        lines = ["Device missing:"] + missing
        show_warning(ev3, "Device Error", lines)
        msg = "Missing devices: {}".format("; ".join(missing))
        log_utils.log(msg)
        raise RuntimeError(msg)

    log_utils.log("Device precheck passed.")


def main():
    ev3 = EV3Brick()
    ev3.light.off()
    if not config.HARDWARE_PRECHECK_ENABLED:
        log_utils.log("Warning: Hardware precheck is disabled.")
    if not config.BATTERY_CHECK_ENABLED:
        log_utils.log("Warning: Battery voltage check is disabled.")
    if config.HARDWARE_PRECHECK_ENABLED:
        precheck_devices(ev3)
    car = Car(auto_calibrate=False, ev3=ev3)
    logger = RunLogger()

    run_config = user_input.get_default_run_config()
    run_config = collect_run_config(car.ev3, car, run_config, runtime_input=user_input.USE_RUNTIME_INPUT)

    if not user_input.USE_RUNTIME_INPUT:
        errors, warnings = config.validate_config(run_config)
        if errors or warnings:
            show_warning(car.ev3, "Config Warning", [e["message"] for e in errors] + warnings)
    strategy = get_strategy(run_config)
    corrected_distance_m = run_config["target_distance_m"] + config.DISTANCE_CORRECTION_M
    log_utils.log("Strategy initialized: {}".format(run_config["mode"]))
    log_utils.log("Target: {:.3f}m (raw {:.3f}m, corr {:+.3f}m) in {:.2f}s".format(
        corrected_distance_m,
        run_config["target_distance_m"],
        config.DISTANCE_CORRECTION_M,
        run_config["target_time_s"],
    ))
    if run_config["mode"] == config.MODE_BONUS:
        log_utils.log("Bonus gap: {}m".format(run_config["bonus_gap_m"]))
    wait(200)

    event_timer = StopWatch()
    event_timer.reset()
    logger.event(event_timer.time(), "ready")
    log_utils.log("Run start.")
    logger.event(event_timer.time(), "start")
    car.ev3.light.off()

    car.reset_odometry()
    run_timer = StopWatch(); run_timer.reset()
    last_log_ms = 0
    last_progress_ms = 0
    log_interval_ms = run_config.get("log_interval_ms", config.LOG_INTERVAL_MS)

    max_run_ms = int(strategy.target_time_s * 2000)  # 2.0x target time guard
    stall_threshold_mm = 5.0
    stall_window_ms = 1200
    last_move_ms = 0
    last_dist_mm = 0.0
    loop_ms = 0
    dist_mm = 0.0

    while not strategy.is_finished(run_timer.time() / 1000.0):
        loop_ms = run_timer.time()
        time_s = loop_ms / 1000.0

        if (loop_ms // 500) % 2 == 0:
            car.ev3.light.on(config.Color.GREEN)
        else:
            car.ev3.light.off()

        car.update_sensors()

        dist_mm = car.get_distance()
        target_v, target_h = strategy.get_target_state(time_s, dist_mm)

        car.drive_speed(target_v)
        car.steer_heading(target_h)

        if loop_ms - last_log_ms >= log_interval_ms:
            heading = car.get_heading()
            logger.state(loop_ms, dist_mm, target_v, target_h, heading, car.drift_rate_dps)
            log_utils.log("Telemetry: t={:.2f}s, d={:.1f}mm, v={:.1f}mm/s, h={:.1f}deg".format(time_s, dist_mm, target_v, heading))
            last_log_ms = loop_ms

        if loop_ms - last_progress_ms >= 150:
            progress_fraction = min(1.0, dist_mm / max(1.0, strategy.total_path_length))
            show_progress(car.ev3, run_config.get("mode"), progress_fraction, time_s)
            last_progress_ms = loop_ms

        # Stall detection: if movement < threshold over window, stop.
        if loop_ms - last_move_ms >= stall_window_ms:
            if abs(dist_mm - last_dist_mm) < stall_threshold_mm:
                log_utils.log("Stall detected.")
                logger.event(event_timer.time(), "stall_detected")
                break
            last_move_ms = loop_ms
            last_dist_mm = dist_mm

        # Absolute runtime guard
        if loop_ms >= max_run_ms:
            log_utils.log("Timeout guard activated.")
            logger.event(event_timer.time(), "timeout_guard")
            break

        wait(10)

    logger.event(event_timer.time(), "complete")
    car.stop(brake=True)
    car.ev3.light.on(config.Color.RED)

    total_time_s = loop_ms / 1000.0
    log_utils.log("Run complete.")
    log_utils.log("Distance: {:.3f} m".format(dist_mm / 1000.0))
    log_utils.log("Time: {:.3f} s".format(total_time_s))
    if "target_time_s" in run_config:
        error_s = total_time_s - run_config["target_time_s"]
        log_utils.log("Time err: {:.3f} s".format(error_s))
    show_summary(car.ev3, run_config.get("mode"), dist_mm / 1000.0, total_time_s, run_config.get("target_time_s"))
    log_utils.log("Press center to dismiss summary.")
    while Button.CENTER not in car.ev3.buttons.pressed():
        wait(20)


if __name__ == "__main__":
    main()