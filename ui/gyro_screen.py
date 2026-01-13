"""Gyro calibration screen."""

from .common import render_value_page, mark_complete


class GyroScreen:
    key = "gyro_calibration"
    shape = "square"

    def __init__(self, car):
        self.car = car

    def render(self, ev3, state, steps, current_index):
        drift = state.get("drift_dps", self.car.drift_rate_dps)
        value_text = "Drift {:.4f} dps".format(drift)
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
        drift = self.car.calibrate_gyro_drift()
        state["drift_dps"] = drift
        mark_complete(state, self.key)
