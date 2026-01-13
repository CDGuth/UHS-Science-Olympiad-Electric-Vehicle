#!/usr/bin/env pybricks-micropython
"""Main execution entry point for the Science Olympiad Electric Vehicle 2026."""

from pybricks.parameters import Button  # pyright: ignore[reportMissingImports]
from pybricks.tools import wait, StopWatch  # pyright: ignore[reportMissingImports]

import config
import user_input
from vehicle import Car
from strategies import get_strategy
from run_logger import RunLogger
from ui.ui_flow import collect_run_config
from ui.run_status import show_progress, show_summary


def main():
    car = Car(auto_calibrate=not user_input.USE_RUNTIME_INPUT)
    logger = RunLogger()

    run_config = user_input.get_default_run_config()
    if user_input.USE_RUNTIME_INPUT:
        run_config = collect_run_config(car.ev3, car, run_config)

    config.validate_config(run_config)
    strategy = get_strategy(run_config)
    print("strategy initialized: {}".format(run_config["mode"]))
    print("target: {}m in {}s".format(run_config["target_distance_m"], run_config["target_time_s"]))
    if run_config["mode"] == config.MODE_BONUS:
        print("bonus gap: {}m".format(run_config["bonus_gap_m"]))

    car.ev3.light.on(config.Color.GREEN)
    wait(200)

    event_timer = StopWatch()
    event_timer.reset()
    logger.event(event_timer.time(), "ready")
    print("press center button to start the run")

    while Button.CENTER not in car.ev3.buttons.pressed():
        wait(10)

    while Button.CENTER in car.ev3.buttons.pressed():
        wait(10)

    print("run start")
    logger.event(event_timer.time(), "start")
    car.ev3.light.on(config.Color.RED)

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

    while not strategy.is_finished(run_timer.time() / 1000.0):
        loop_ms = run_timer.time()
        time_s = loop_ms / 1000.0

        car.update_sensors()

        dist_mm = car.get_distance()
        target_v, target_h = strategy.get_target_state(time_s, dist_mm)

        car.drive_speed(target_v)
        car.steer_heading(target_h)

        if loop_ms - last_log_ms >= log_interval_ms:
            heading = car.get_heading()
            logger.state(loop_ms, dist_mm, target_v, target_h, heading, car.drift_rate_dps)
            print("t: {:.2f}s, d: {:.1f}mm, v: {:.1f}mm/s, h: {:.1f}deg".format(time_s, dist_mm, target_v, heading))
            last_log_ms = loop_ms

        if loop_ms - last_progress_ms >= 150:
            progress_fraction = min(1.0, dist_mm / max(1.0, strategy.total_path_length))
            show_progress(car.ev3, run_config.get("mode"), progress_fraction, time_s)
            last_progress_ms = loop_ms

        # Stall detection: if movement < threshold over window, stop.
        if loop_ms - last_move_ms >= stall_window_ms:
            if abs(dist_mm - last_dist_mm) < stall_threshold_mm:
                print("stall detected")
                logger.event(event_timer.time(), "stall_detected")
                break
            last_move_ms = loop_ms
            last_dist_mm = dist_mm

        # Absolute runtime guard
        if loop_ms >= max_run_ms:
            print("timeout guard activated")
            logger.event(event_timer.time(), "timeout_guard")
            break

        wait(10)

    logger.event(event_timer.time(), "complete")
    car.stop(brake=True)

    total_time_s = loop_ms / 1000.0
    print("run complete")
    print("distance: {:.3f} m".format(dist_mm / 1000.0))
    print("time: {:.3f} s".format(total_time_s))
    if "target_time_s" in run_config:
        error_s = total_time_s - run_config["target_time_s"]
        print("time err: {:.3f} s".format(error_s))
    show_summary(car.ev3, run_config.get("mode"), dist_mm / 1000.0, total_time_s, run_config.get("target_time_s"))
    print("press center to dismiss summary")
    while Button.CENTER not in car.ev3.buttons.pressed():
        wait(20)
    car.ev3.light.on(config.Color.ORANGE)
    car.ev3.speaker.beep()
    wait(5000)


if __name__ == "__main__":
    main()