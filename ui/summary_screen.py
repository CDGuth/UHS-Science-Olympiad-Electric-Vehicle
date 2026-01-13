"""Final confirmation and start screen."""

from .common import TITLE_FONT, VALUE_FONT, HINT_FONT, draw_indicator_bar, draw_play_shape, mark_complete


class SummaryScreen:
    key = "start_run"
    shape = "play"

    def render(self, ev3, state, steps, current_index):
        lines = [
            "Mode: {}".format(state.get("mode")),
            "Dist: {:.2f} m".format(state.get("target_distance_m", 0.0)),
            "Time: {:.2f} s".format(state.get("target_time_s", 0.0)),
            "Gap:  {:.2f} m".format(state.get("bonus_gap_m", 0.0)),
            "Center: start run",
        ]
        screen = ev3.screen
        screen.clear()
        screen.set_font(TITLE_FONT)
        screen.draw_text(6, 6, "Ready to Run")
        draw_play_shape(screen, 150, 22, 11, state.get("completed", {}).get(self.key, False))

        screen.set_font(VALUE_FONT)
        y = 28
        for line in lines:
            screen.draw_text(6, y, line)
            y += 14
        screen.set_font(HINT_FONT)

        draw_indicator_bar(ev3, steps, current_index, state.get("completed", {}))

    def on_up(self, state, step=None):
        return None

    def on_down(self, state, step=None):
        return None

    def on_center(self, state):
        mark_complete(state, self.key)
        return "start"
