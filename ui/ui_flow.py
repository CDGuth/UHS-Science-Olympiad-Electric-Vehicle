"""EV3 brick UI flow for collecting run configuration."""

from pybricks.parameters import Button  # pyright: ignore[reportMissingImports]
from pybricks.tools import wait, StopWatch  # pyright: ignore[reportMissingImports]

import config
import user_input

from .mode_screen import ModeScreen
from .distance_screen import DistanceScreen
from .time_screen import TimeScreen
from .bonus_screen import BonusScreen
from .gyro_screen import GyroScreen
from .summary_screen import SummaryScreen
from .common import mark_complete


def _debounce_buttons(ev3):
    while ev3.buttons.pressed():
        wait(50)


def collect_run_config(ev3, car, initial_config):
    """
    Interactive flow that returns a run_config dict.
    Screens use Up/Down for value changes and Left/Right to navigate.
    """
    def build_screens(current_mode):
        base = [ModeScreen(), DistanceScreen(), TimeScreen()]
        if current_mode == config.MODE_BONUS:
            base.append(BonusScreen())
        base.append(GyroScreen(car))
        base.append(SummaryScreen())
        return base

    state = dict(initial_config)
    state.setdefault("bonus_gap_m", 0.0)
    state.setdefault("drift_dps", car.drift_rate_dps)
    state["distance_step"] = user_input.get_distance_step()
    state["distance_fast_step"] = 1.0
    state["time_step"] = user_input.get_time_step()
    state["time_fast_step"] = 1.0
    state["bonus_step"] = 0.05
    state["bonus_fast_step"] = 0.25

    index = 0
    timer = StopWatch(); timer.reset()
    press_start = {Button.UP: None, Button.DOWN: None}
    last_repeat = {Button.UP: 0, Button.DOWN: 0}
    prev_pressed = {Button.UP: False, Button.DOWN: False}
    debounce_ms = 50
    repeat_ms = 180
    hold_accel_ms = 3000

    while True:
        screens = build_screens(state.get("mode", config.MODE_STRAIGHT))
        steps = [{"key": s.key, "shape": s.shape} for s in screens]
        state.setdefault("completed", {})
        for s in screens:
            state["completed"].setdefault(s.key, False)

        if index >= len(screens):
            index = len(screens) - 1

        screens[index].render(ev3, state, steps, index)
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
                held_ms = now - (press_start.get(button) or now)
                factor = accel_factor(scr.key, held_ms)
                if last_repeat[button] == 0 or now - last_repeat[button] >= repeat_ms:
                    step = base * factor
                    up_fn(step)
                    last_repeat[button] = now
                prev_pressed[button] = True
            else:
                prev_pressed[button] = False
                press_start[button] = None
                last_repeat[button] = 0

        current_screen = screens[index]
        handle_step(Button.UP, current_screen, lambda step: current_screen.on_up(state, step))
        handle_step(Button.DOWN, current_screen, lambda step: current_screen.on_down(state, step))

        # Center press is immediate action; no extra confirmation needed.
        if Button.CENTER in pressed:
            action = screens[index].on_center(state)
            _debounce_buttons(ev3)
            if action == "start":
                mark_complete(state, screens[index].key)
                return {
                    "mode": state.get("mode"),
                    "target_distance_m": state.get("target_distance_m"),
                    "target_time_s": state.get("target_time_s"),
                    "bonus_gap_m": state.get("bonus_gap_m", 0.0),
                }

    return initial_config
