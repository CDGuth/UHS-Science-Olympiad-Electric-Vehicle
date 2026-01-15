"""Bonus can gap selection screen."""

import config
from .common import clamp, render_value_page, mark_complete, mark_incomplete, is_complete


class BonusScreen:
    key = "bonus_gap_m"
    shape = "circle"

    def render(self, ev3, state, steps, current_index):
        value = state.get("bonus_gap_m", 0.0)
        value_text = "{:.2f} m".format(value)
        step = state.get("bonus_step", 0.05)
        fast_step = state.get("bonus_fast_step", 0.25)
        if is_complete(state, self.key):
            hints = ["Center: unlock to edit"]
        else:
            hints = [
                "Up/Down: +/-{:.2f} m".format(step),
                "Hold>3s: faster", 
                "Center: mark complete",
            ]
        render_value_page(ev3, "Bonus Gap", value_text, hints, steps, current_index, state.get("completed", {}))

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
        value = state.get("bonus_gap_m", 0.0) + delta
        if config.VALIDATION_ENABLED:
            value = clamp(value, 0.0, 1.0)
        state["bonus_gap_m"] = round(value, 3)
