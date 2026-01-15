"""Final confirmation screen for run settings."""

from .common import TITLE_FONT, DEFAULT_FONT, HINT_FONT, SCREEN_HEIGHT, draw_indicator_bar


class ConfirmationScreen:
    key = "confirm_run"
    shape = "play"

    def render(self, ev3, state, steps, current_index):
        screen = ev3.screen
        screen.clear()

        screen.set_font(TITLE_FONT)
        screen.draw_text(6, 6, "Confirm Run Profile:")

        rows = [
            ("Mode", "{}".format(state.get("mode"))),
            ("Distance", "{:.2f} m".format(state.get("target_distance_m", 0.0))),
            ("Time", "{:.2f} s".format(state.get("target_time_s", 0.0))),
            ("Bonus Gap", "{:.2f} m".format(state.get("bonus_gap_m", 0.0))),
        ]

        y = 22
        for label, value in rows:
            screen.set_font(DEFAULT_FONT)
            screen.draw_text(6, y, label + ":")
            screen.draw_text(96, y, value)
            y += 16

        screen.set_font(HINT_FONT)
        screen.draw_text(6, SCREEN_HEIGHT - 40, "Center: confirm run profile")

        draw_indicator_bar(ev3, steps, current_index, state.get("completed", {}))

    def on_up(self, state, step=None):
        return None

    def on_down(self, state, step=None):
        return None

    def on_center(self, state):
        return "confirm"