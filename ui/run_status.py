"""Run-time status screens for progress and summary."""

from pybricks.media.ev3dev import Font  # pyright: ignore[reportMissingImports]
from .common import SCREEN_WIDTH, SCREEN_HEIGHT

TITLE_FONT = Font(size=16)
VALUE_FONT = Font(size=14)
SMALL_FONT = Font(size=10)


def _draw_bar(screen, x, y, w, h, fraction):
    fraction = max(0.0, min(1.0, fraction))
    fill_w = int(w * fraction)
    # Border
    screen.draw_line(x, y, x + w, y)
    screen.draw_line(x, y + h - 1, x + w, y + h - 1)
    screen.draw_line(x, y, x, y + h - 1)
    screen.draw_line(x + w, y, x + w, y + h - 1)
    # Fill
    for dy in range(1, h - 1):
        if fill_w > 0:
            screen.draw_line(x + 1, y + dy, x + fill_w, y + dy)


def show_progress(ev3, mode, progress_fraction, time_s):
    screen = ev3.screen
    screen.clear()
    screen.set_font(TITLE_FONT)
    screen.draw_text(6, 4, "Run Progress")
    screen.set_font(VALUE_FONT)
    screen.draw_text(6, 24, "Mode: {}".format(mode))
    screen.draw_text(6, 40, "Time: {:.2f}s".format(time_s))
    _draw_bar(screen, 6, 64, SCREEN_WIDTH - 12, 12, progress_fraction)


def show_summary(ev3, mode, distance_m, time_s, target_time_s):
    screen = ev3.screen
    screen.clear()
    screen.set_font(TITLE_FONT)
    screen.draw_text(6, 4, "Run Summary")
    screen.set_font(VALUE_FONT)
    screen.draw_text(6, 24, "Mode: {}".format(mode))
    screen.draw_text(6, 40, "Dist: {:.2f} m".format(distance_m))
    screen.draw_text(6, 56, "Time: {:.2f} s".format(time_s))
    if target_time_s is not None:
        err = time_s - target_time_s
        screen.draw_text(6, 72, "Time err: {:+.2f} s".format(err))
    screen.set_font(SMALL_FONT)
    screen.draw_text(6, 92, "Center to dismiss")