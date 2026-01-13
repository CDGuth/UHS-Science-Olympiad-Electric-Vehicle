"""Mode selection screen."""

import config
from .common import render_value_page, mark_complete, mark_incomplete, is_complete


class ModeScreen:
	key = "mode"
	shape = "circle"

	def render(self, ev3, state, steps, current_index):
		value = state.get("mode", config.MODE_STRAIGHT)
		if is_complete(state, self.key):
			hints = ["Center: unlock to edit"]
		else:
			hints = ["Up/Down: switch mode", "Center: mark complete"]
		render_value_page(ev3, "Run Mode", value, hints, steps, current_index, state.get("completed", {}))

	def on_up(self, state, step=None):
		if is_complete(state, self.key):
			return
		self._toggle(state)

	def on_down(self, state, step=None):
		if is_complete(state, self.key):
			return
		self._toggle(state)

	def on_center(self, state):
		if is_complete(state, self.key):
			mark_incomplete(state, self.key)
		else:
			mark_complete(state, self.key)
		return None

	def _toggle(self, state):
		current = state.get("mode", config.MODE_STRAIGHT)
		state["mode"] = config.MODE_BONUS if current == config.MODE_STRAIGHT else config.MODE_STRAIGHT
