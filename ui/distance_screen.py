"""Target distance selection screen."""

import config
import user_input
from .common import clamp, render_value_page, mark_complete, mark_incomplete, is_complete


class DistanceScreen:
    key = "target_distance_m"
    shape = "circle"

    def render(self, ev3, state, steps, current_index):
        value = state.get("target_distance_m", config.MIN_TARGET_DISTANCE_M)
        value_text = "{:.2f} m".format(value)
        step = state.get("distance_step", user_input.get_distance_step())
        fast_step = state.get("distance_fast_step", 1.0)
        if is_complete(state, self.key):
            hints = ["Center: unlock to edit"]
        else:
            hints = [
                "Up/Down: +/-{:.2f} m".format(step),
                "Hold>3s: faster", 
                "Center: mark complete",
            ]
        render_value_page(ev3, "Target Distance", value_text, hints, steps, current_index, state.get("completed", {}))

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
        value = state.get("target_distance_m", 0.0) + delta
        if config.VALIDATION_ENABLED:
            value = clamp(value, config.MIN_TARGET_DISTANCE_M, config.MAX_TARGET_DISTANCE_M)
        state["target_distance_m"] = round(value, 3)
