"""EV3 brick UI flow for collecting run configuration."""

from pybricks.parameters import Button  # pyright: ignore[reportMissingImports]
from pybricks.tools import wait, StopWatch  # pyright: ignore[reportMissingImports]

import config
import user_input
import log_utils

from .mode_screen import ModeScreen
from .distance_screen import DistanceScreen
from .time_screen import TimeScreen
from .bonus_screen import BonusScreen
from .gyro_screen import GyroScreen
from .steering_screen import SteeringScreen
from .confirmation_screen import ConfirmationScreen
from .ready_screen import ReadyScreen
from .common import mark_complete, show_warning


def _debounce_buttons(ev3):
    while ev3.buttons.pressed():
        wait(50)


def collect_run_config(ev3, car, initial_config, runtime_input=True):
    """
    Interactive flow that returns a run_config dict.
    Screens use Up/Down for value changes and Left/Right to navigate.
    """
    def build_screens(current_mode):
        screens = []
        if runtime_input:
            screens.extend([ModeScreen(), DistanceScreen(), TimeScreen()])
            if current_mode == config.MODE_BONUS:
                screens.append(BonusScreen())
        screens.append(GyroScreen(car))
        if car.steer_motor is not None:
            screens.append(SteeringScreen(car))
        screens.append(ConfirmationScreen())
        screens.append(ReadyScreen())
        return screens

    state = dict(initial_config)
    state.setdefault("bonus_gap_m", 0.0)
    state.setdefault("drift_dps", car.drift_rate_dps)
    state["distance_step"] = user_input.get_distance_step()
    state["distance_fast_step"] = 1.0
    state["time_step"] = user_input.get_time_step()
    state["time_fast_step"] = 1.0
    state["bonus_step"] = 0.05
    state["bonus_fast_step"] = 0.25

    key_labels = {
        "mode": "Run Mode",
        "target_distance_m": "Target Distance",
        "target_time_s": "Target Time",
        "bonus_gap_m": "Bonus Gap",
        "gyro_calibration": "Gyro Calibration",
        "steering_calibration": "Steering Align",
        "confirm_run": "Confirm Run",
    }

    def current_run_config(state):
        return {
            "mode": state.get("mode"),
            "target_distance_m": state.get("target_distance_m"),
            "target_time_s": state.get("target_time_s"),
            "bonus_gap_m": state.get("bonus_gap_m", 0.0),
        }

    def first_incomplete_index(screens, state):
        for i, scr in enumerate(screens):
            if scr.key in ("confirm_run", "ready_run"):
                continue
            if not state.get("completed", {}).get(scr.key, False):
                return i
        return 0

    def ready_index(screens):
        for i, scr in enumerate(screens):
            if scr.key == "ready_run":
                return i
        return len(screens) - 1

    index = 0
    timer = StopWatch(); timer.reset()
    press_start = {Button.UP: 0, Button.DOWN: 0}
    last_repeat = {Button.UP: 0, Button.DOWN: 0}
    prev_pressed = {Button.UP: False, Button.DOWN: False}
    debounce_ms = 50
    repeat_ms = 180
    hold_accel_ms = 3000

    while True:
        screens = build_screens(state.get("mode", config.MODE_STRAIGHT))
        nav_screens = [s for s in screens if getattr(s, "show_in_nav", True)]
        steps = [{"key": s.key, "shape": s.shape} for s in nav_screens]
        state.setdefault("completed", {})
        for s in screens:
            state["completed"].setdefault(s.key, False)

        if index >= len(screens):
            index = len(screens) - 1

        current_screen = screens[index]
        if current_screen in nav_screens:
            nav_index = nav_screens.index(current_screen)
        else:
            nav_index = len(nav_screens) - 1 if nav_screens else 0

        current_screen.render(ev3, state, steps, nav_index)
        wait(debounce_ms)
        pressed = ev3.buttons.pressed()
        now = timer.time()

        if Button.LEFT in pressed and index > 0:
            index -= 1
            _debounce_buttons(ev3)
            continue
        if Button.RIGHT in pressed and index < len(screens) - 1:
            index += 1
            _debounce_buttons(ev3)
            continue

        def step_sizes_for_screen(scr):
            if scr.key == "target_distance_m":
                return state.get("distance_step", 0.1)
            if scr.key == "target_time_s":
                return state.get("time_step", 0.1)
            if scr.key == "bonus_gap_m":
                return state.get("bonus_step", 0.05)
            return 1.0

        def accel_factor(scr_key, held_ms):
            if held_ms < hold_accel_ms:
                return 1.0
            if scr_key == "target_time_s":
                return 5.0
            if scr_key == "target_distance_m":
                lvl = user_input.EVENT_LEVEL.upper()
                if lvl in ("STATE", "NATIONAL"):
                    return 5.0
                return 4.0
            if scr_key == "bonus_gap_m":
                return 2.0
            return 1.0

        def handle_step(button, scr, up_fn):
            base = step_sizes_for_screen(scr)
            if button in pressed:
                if not prev_pressed[button]:
                    press_start[button] = now
                    last_repeat[button] = 0
                held_ms = now - press_start[button]
                factor = accel_factor(scr.key, held_ms)
                if last_repeat[button] == 0 or now - last_repeat[button] >= repeat_ms:
                    step = base * factor
                    up_fn(step)
                    last_repeat[button] = now
                prev_pressed[button] = True
            else:
                prev_pressed[button] = False
                press_start[button] = 0
                last_repeat[button] = 0

        handle_step(Button.UP, current_screen, lambda step: current_screen.on_up(state, step))
        handle_step(Button.DOWN, current_screen, lambda step: current_screen.on_down(state, step))

        # Center press is immediate action; no extra confirmation needed.
        if Button.CENTER in pressed:
            action = screens[index].on_center(state)
            _debounce_buttons(ev3)
            if action == "confirm":
                missing = [
                    scr.key
                    for scr in screens
                    if scr.key not in ("confirm_run", "ready_run")
                    and not state.get("completed", {}).get(scr.key, False)
                ]
                if missing:
                    lines = ["Complete before confirm:"] + [key_labels.get(k, k) for k in missing]
                    show_warning(ev3, "Complete Steps", lines)
                    index = first_incomplete_index(screens, state)
                    continue

                run_config = current_run_config(state)
                errors, warnings = config.validate_config(run_config)

                if errors and runtime_input:
                    show_warning(ev3, "Fix Config", [e["message"] for e in errors])
                    fatal_errors = [e for e in errors if not e.get("fixable")]
                    for err in errors:
                        key = err.get("key")
                        if err.get("fixable") and key and key in state.get("completed", {}):
                            state["completed"][key] = False
                    if fatal_errors:
                        raise RuntimeError("Non-fixable config error: {}".format(
                            "; ".join(e.get("message", "unknown") for e in fatal_errors)
                        ))
                    index = first_incomplete_index(screens, state)
                    continue

                if errors and not runtime_input:
                    show_warning(ev3, "Config Warning", [e["message"] for e in errors])

                if warnings:
                    show_warning(ev3, "Config Warning", warnings)

                mark_complete(state, screens[index].key)
                log_utils.log(
                    "Run confirmed: mode={}, dist={:.2f}m, time={:.2f}s, gap={:.2f}m".format(
                        run_config.get("mode"),
                        run_config.get("target_distance_m", 0.0),
                        run_config.get("target_time_s", 0.0),
                        run_config.get("bonus_gap_m", 0.0),
                    )
                )
                index = ready_index(screens)
                continue

            if action == "start":
                if not state.get("completed", {}).get("confirm_run", False):
                    show_warning(ev3, "Confirm First", ["Confirm run profile first."])
                    index = ready_index(screens) - 1
                    continue
                return current_run_config(state)

    return initial_config
