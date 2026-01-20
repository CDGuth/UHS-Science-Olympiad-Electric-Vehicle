"""Post-run summary UI."""

from .common import TITLE_FONT, DEFAULT_FONT, HINT_FONT, SCREEN_HEIGHT


def show_summary(ev3, mode, distance_m, time_s, target_time_s, distance_error_m=None):
    """Render the post-run summary screen."""
    screen = ev3.screen
    screen.clear()
    screen.set_font(TITLE_FONT)
    screen.draw_text(6, 4, "Run Summary")

    screen.set_font(DEFAULT_FONT)
    screen.draw_text(6, 24, "Mode: {}".format(mode))
    screen.draw_text(6, 40, "Dist: {:.2f} m".format(distance_m))
    if distance_error_m is not None:
        screen.draw_text(6, 56, "Dist err: {:.3f} m".format(distance_error_m))
    
    screen.draw_text(6, 72, "Time: {:.2f} s".format(time_s))
    if target_time_s is not None:
        err = time_s - target_time_s
        screen.draw_text(6, 88, "Time err: {:+.2f} s".format(err))

    screen.set_font(HINT_FONT)
    screen.draw_text(6, SCREEN_HEIGHT - 16, "Center to dismiss")
