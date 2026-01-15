"""Shared UI helpers for EV3 brick screens."""

from pybricks.parameters import Color, Button  # pyright: ignore[reportMissingImports]
from pybricks.media.ev3dev import Font  # pyright: ignore[reportMissingImports]
from pybricks.tools import wait  # pyright: ignore[reportMissingImports]

SCREEN_WIDTH = 178
SCREEN_HEIGHT = 128
INDICATOR_Y = 115
INDICATOR_SIZE = 6
INDICATOR_MARGIN = 10
INDICATOR_THICKNESS = 2

TITLE_FONT = Font(size=16)
VALUE_FONT = Font(size=18)
DEFAULT_FONT = Font(size=14)
HINT_FONT = Font(size=10)


def _wrap_line(line, width):
    words = line.split()
    if not words:
        return [""]
    rows = []
    current = words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            rows.append(current)
            current = word
    rows.append(current)
    # Handle very long single words
    flat_rows = []
    for row in rows:
        if len(row) <= width:
            flat_rows.append(row)
        else:
            start = 0
            while start < len(row):
                flat_rows.append(row[start:start + width])
                start += width
    return flat_rows


def wrap_text_lines(lines, width=24):
    wrapped = []
    for line in lines:
        wrapped.extend(_wrap_line(line, width))
    return wrapped


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def _draw_hline_thick(screen, x1, x2, y, thickness):
    half = thickness // 2
    for dy in range(-half, half + 1):
        screen.draw_line(x1, y + dy, x2, y + dy)


def draw_circle_shape(screen, x, y, radius, filled, thickness=INDICATOR_THICKNESS):
    if radius <= 0:
        return
    if filled:
        for dy in range(-radius, radius + 1):
            dx = int((radius * radius - dy * dy) ** 0.5)
            _draw_hline_thick(screen, x - dx, x + dx, y + dy, 1)
        for t in range(thickness):
            r = radius - t
            if r > 0:
                screen.draw_circle(x, y, r)
    else:
        for t in range(thickness):
            r = radius - t
            if r > 0:
                screen.draw_circle(x, y, r)


def draw_square_shape(screen, x, y, size, filled, thickness=INDICATOR_THICKNESS):
    half = size // 2
    if half <= 0:
        return
    if filled:
        for dy in range(-half, half + 1):
            _draw_hline_thick(screen, x - half, x + half, y + dy, 1)
    for t in range(thickness):
        inset = t
        if half - inset <= 0:
            break
        screen.draw_line(x - half + inset, y - half + inset, x + half - inset, y - half + inset)
        screen.draw_line(x - half + inset, y + half - inset, x + half - inset, y + half - inset)
        screen.draw_line(x - half + inset, y - half + inset, x - half + inset, y + half - inset)
        screen.draw_line(x + half - inset, y - half + inset, x + half - inset, y + half - inset)


def draw_triangle_shape(screen, x, y, size, filled, thickness=INDICATOR_THICKNESS):
    half = size // 2
    if half <= 0:
        return
    if filled:
        for dy in range(-half, half + 1):
            span = size - abs(dy)
            start_x = x - half
            end_x = start_x + span
            _draw_hline_thick(screen, start_x, end_x, y + dy, 1)
    for t in range(thickness):
        inset = t
        screen.draw_line(x - half + inset, y + half - inset, x + half - inset, y - inset)
        screen.draw_line(x + half - inset, y - inset, x - half + inset, y - half + inset)
        screen.draw_line(x - half + inset, y - half + inset, x - half + inset, y + half - inset)


def draw_play_shape(screen, x, y, radius, completed):
    if completed:
        draw_circle_shape(screen, x, y, radius, True)
    draw_circle_shape(screen, x, y, radius, False)
    tri_size = max(4, radius)
    half = tri_size // 2
    for dy in range(-half, half + 1):
        proportion = 1 - abs(dy) / max(1, half)
        dx = int(tri_size * proportion)
        start_x = x - half + 1
        end_x = start_x + dx
        _draw_hline_thick(screen, start_x, end_x, y + dy, 1)


def draw_indicator_bar(ev3, steps, current_index, completed_map):
    screen = ev3.screen
    count = len(steps)
    if count == 0:
        return

    usable = SCREEN_WIDTH - 2 * INDICATOR_MARGIN
    spacing = usable // (count - 1 if count > 1 else 1)
    positions = [INDICATOR_MARGIN + spacing * i for i in range(count)]

    # Connectors
    for i in range(count - 1):
        start_x = positions[i] + INDICATOR_SIZE + 1
        end_x = positions[i + 1] - INDICATOR_SIZE - 1
        _draw_hline_thick(screen, start_x, end_x, INDICATOR_Y, INDICATOR_THICKNESS)

    # Nodes
    for i, step in enumerate(steps):
        x = positions[i]
        filled = completed_map.get(step["key"], False)
        shape = step["shape"]
        if shape == "circle":
            draw_circle_shape(screen, x, INDICATOR_Y, INDICATOR_SIZE, filled)
        elif shape == "square":
            draw_square_shape(screen, x, INDICATOR_Y, INDICATOR_SIZE * 2, filled)
        elif shape == "triangle":
            draw_triangle_shape(screen, x, INDICATOR_Y, INDICATOR_SIZE * 2, filled)
        elif shape == "play":
            draw_play_shape(screen, x, INDICATOR_Y, INDICATOR_SIZE, filled)

        # Highlight current step with a thicker underline mark, slightly lower for breathing room.
        if i == current_index:
            _draw_hline_thick(screen, x - INDICATOR_SIZE, x + INDICATOR_SIZE, INDICATOR_Y + INDICATOR_SIZE + 5, INDICATOR_THICKNESS + 1)


def render_value_page(ev3, title, value_text, hint_lines, steps, current_index, completed_map):
    screen = ev3.screen
    screen.clear()
    screen.set_font(TITLE_FONT)
    screen.draw_text(6, 4, title)
    screen.set_font(VALUE_FONT)
    screen.draw_text(6, 26, value_text)

    screen.set_font(HINT_FONT)
    y = 54
    for line in hint_lines:
        screen.draw_text(6, y, line)
        y += 12
    screen.set_font(DEFAULT_FONT)

    draw_indicator_bar(ev3, steps, current_index, completed_map)


def mark_complete(state, key):
    state.setdefault("completed", {})[key] = True


def is_complete(state, key):
    return state.get("completed", {}).get(key, False)


def mark_incomplete(state, key):
    state.setdefault("completed", {})[key] = False


def show_warning(ev3, title, lines):
    """Display a blocking warning dialog and wait for center press."""
    screen = ev3.screen
    screen.clear()
    screen.set_font(TITLE_FONT)
    screen.draw_text(6, 4, title)
    screen.set_font(DEFAULT_FONT)

    wrapped = wrap_text_lines(lines, width=24)
    y = 26
    for line in wrapped:
        screen.draw_text(6, y, line)
        y += 14

    screen.set_font(HINT_FONT)
    screen.draw_text(6, SCREEN_HEIGHT - 14, "Center to continue")

    while True:
        if Button.CENTER in ev3.buttons.pressed():
            break
        wait(50)
    while Button.CENTER in ev3.buttons.pressed():
        wait(50)
