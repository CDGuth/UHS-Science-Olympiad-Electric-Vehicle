"""Target time selection screen."""

import config
import user_input
from .common import clamp, render_value_page, mark_complete, mark_incomplete, is_complete


class TimeScreen:
    key = "target_time_s"
    shape = "circle"

    def render(self, ev3, state, steps, current_index):
        value = state.get("target_time_s", config.MIN_TARGET_TIME_S)
        value_text = "{:.2f} s".format(value)
        step = state.get("time_step", user_input.get_time_step())
        fast_step = state.get("time_fast_step", 1.0)
        if is_complete(state, self.key):
            hints = ["Center: unlock to edit"]
        else:
            hints = [
                "Up/Down: +/-{:.2f} s".format(step),
                "Hold>3s: faster", 
                "Center: mark complete",
            ]
        render_value_page(ev3, "Target Time", value_text, hints, steps, current_index, state.get("completed", {}))

    def on_up(self, state, step):
        if is_complete(state, self.key):
            return
        self._adjust(state, step)

    def on_down(self, state, step):
        if is_complete(state, self.key):
            return
        self._adjust(state, -step)

    def on_center(self, state):
        if is_complete(state, self.key):
            mark_incomplete(state, self.key)
        else:
            mark_complete(state, self.key)
        return None

    def _adjust(self, state, delta):
        value = state.get("target_time_s", 0.0) + delta
        if config.VALIDATION_ENABLED:
            value = clamp(value, config.MIN_TARGET_TIME_S, config.MAX_TARGET_TIME_S)
        state["target_time_s"] = round(value, 3)
