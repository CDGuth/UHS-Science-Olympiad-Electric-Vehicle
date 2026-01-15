"""Ready-to-run screen displayed after confirming settings."""

from pybricks.media.ev3dev import Font  # pyright: ignore[reportMissingImports]
from pybricks.parameters import Color  # pyright: ignore[reportMissingImports]
from pybricks.tools import StopWatch  # pyright: ignore[reportMissingImports]

from .common import HINT_FONT, SCREEN_HEIGHT, SCREEN_WIDTH

READY_FONT = Font(size=20)


class ReadyScreen:
    key = "ready_run"
    shape = "play"
    show_in_nav = False

    def __init__(self):
        self._blink = StopWatch()
        self._blink.reset()
        self._ev3 = None

    def render(self, ev3, state, steps, current_index):
        self._ev3 = ev3
        screen = ev3.screen
        screen.clear()
        screen.set_font(READY_FONT)
        title = "READY TO RUN"
        title_width = READY_FONT.text_width(title)
        title_x = max(0, (SCREEN_WIDTH - title_width) // 2)
        title_y = 22
        screen.draw_text(title_x, title_y, title)
        screen.draw_text(title_x + 1, title_y, title)

        if (self._blink.time() // 300) % 2 == 0:
            ev3.light.on(Color.GREEN)
        else:
            ev3.light.off()

        screen.set_font(HINT_FONT)
        hint = "Center: begin run"
        hint_width = HINT_FONT.text_width(hint)
        hint_x = max(0, (SCREEN_WIDTH - hint_width) // 2)
        screen.draw_text(hint_x, SCREEN_HEIGHT - 32, hint)

    def on_up(self, state, step=None):
        return None

    def on_down(self, state, step=None):
        return None

    def on_center(self, state):
        self._blink.reset()
        if self._ev3:
            self._ev3.light.off()
        return "start"
