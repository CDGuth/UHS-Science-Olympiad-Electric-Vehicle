"""Gyro calibration screen."""

import config
import log_utils
from .common import render_value_page, mark_complete, TITLE_FONT, DEFAULT_FONT


class GyroScreen:
    key = "gyro_calibration"
    shape = "square"

    def __init__(self, car):
        self.car = car
        self.ev3 = None

    def render(self, ev3, state, steps, current_index):
        self.ev3 = ev3
        calibrated = state.get("completed", {}).get(self.key, False)
        if calibrated:
            drift = state.get("drift_dps", self.car.drift_rate_dps)
            value_text = "Drift {:.4f} dps".format(drift)
        else:
            value_text = "NOT CALIBRATED"
        hints = ["Up/Down/Center: calibrate", "Keep vehicle still"]
        render_value_page(ev3, "Gyro Drift", value_text, hints, steps, current_index, state.get("completed", {}))

    def on_up(self, state, step=None):
        self._calibrate(state)

    def on_down(self, state, step=None):
        self._calibrate(state)

    def on_center(self, state):
        self._calibrate(state)
        return None

    def _calibrate(self, state):
        progress = None
        if self.ev3:
            progress = lambda frac: self._render_progress(frac)
        drift = self.car.calibrate_gyro_drift(progress_cb=progress)
        state["drift_dps"] = drift
        mark_complete(state, self.key)
        log_utils.log("Gyro calibrated; drift={:.4f} dps".format(drift))

    def _render_progress(self, fraction):
        if not self.ev3:
            return
        frac = max(0.0, min(1.0, fraction))
        screen = self.ev3.screen
        screen.clear()
        screen.set_font(TITLE_FONT)
        screen.draw_text(6, 4, "Gyro Calibration")
        screen.set_font(DEFAULT_FONT)
        screen.draw_text(6, 24, "Keep vehicle still")

        x, y, w, h = 6, 60, 166, 14
        screen.draw_line(x, y, x + w, y)
        screen.draw_line(x, y + h - 1, x + w, y + h - 1)
        screen.draw_line(x, y, x, y + h - 1)
        screen.draw_line(x + w, y, x + w, y + h - 1)
        fill_w = int((w - 2) * frac)
        for dy in range(1, h - 1):
            if fill_w > 0:
                screen.draw_line(x + 1, y + dy, x + 1 + fill_w, y + dy)

        percent = int((frac * 100) // 5 * 5)
        screen.draw_text(6, 84, "{}%".format(percent))
