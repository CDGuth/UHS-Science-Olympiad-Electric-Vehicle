"""Steering alignment calibration screen."""

from pybricks.parameters import Stop  # pyright: ignore[reportMissingImports]
from .common import render_value_page, mark_complete, mark_incomplete, is_complete


class SteeringScreen:
    key = "steering_calibration"
    shape = "square"

    def __init__(self, car):
        self.car = car

    def render(self, ev3, state, steps, current_index):
        locked = is_complete(state, self.key)
        value_text = "LOCKED" if locked else "UNLOCKED"
        hints = ["Center: lock/unlock", "Align wheels straight"]
        render_value_page(ev3, "Steering Align", value_text, hints, steps, current_index, state.get("completed", {}))

        if not locked and self.car.steer_motor:
            self.car.steer_motor.stop(Stop.COAST)

    def on_up(self, state, step=None):
        return None

    def on_down(self, state, step=None):
        return None

    def on_center(self, state):
        if is_complete(state, self.key):
            mark_incomplete(state, self.key)
            if self.car.steer_motor:
                self.car.steer_motor.stop(Stop.COAST)
        else:
            if self.car.steer_motor:
                self.car.steer_motor.stop(Stop.HOLD)
                self.car.steer_motor.reset_angle(0)
                self.car.steer_motor.track_target(0)
            mark_complete(state, self.key)
        return None
