"""
Motion profile and path planning mathematics.
Provides velocity curves and path length calculations.
"""

import math
import log_utils


class SCurveProfile:
    """Acceleration-limited S-curve velocity profile."""

    def __init__(self, distance_mm, total_time_s, max_accel_mm_s2, max_decel_mm_s2, max_speed_mm_s=None):
        self.distance_mm = distance_mm
        self.total_time_s = total_time_s
        self.max_accel = max_accel_mm_s2
        self.max_decel = max_decel_mm_s2
        self.max_speed = max_speed_mm_s

        self.v_max = self._solve_peak_velocity()
        if self.max_speed and self.v_max > self.max_speed:
            raise ValueError("Peak speed exceeds configured maximum.")
        self.t_acc = self.v_max * math.pi / (2 * self.max_accel)
        self.t_dec = self.v_max * math.pi / (2 * self.max_decel)
        self.t_cruise = max(0.0, self.total_time_s - self.t_acc - self.t_dec)

        self.t_end_acc = self.t_acc
        self.t_start_dec = self.t_acc + self.t_cruise
        log_utils.log("Profile: v_max={:.1f} mm/s, t_acc={:.2f}s, t_cruise={:.2f}s, t_dec={:.2f}s".format(
            self.v_max, self.t_acc, self.t_cruise, self.t_dec))

    def _solve_peak_velocity(self):
        """Closed-form solution for peak velocity honoring accel limits and time."""
        a_term = (math.pi / 4.0) * ((1.0 / self.max_accel) + (1.0 / self.max_decel))
        discriminant = self.total_time_s ** 2 - 4 * a_term * self.distance_mm
        if discriminant < 0:
            raise ValueError("Profile infeasible with given acceleration limits and time.")

        root = math.sqrt(discriminant)
        v1 = (self.total_time_s - root) / (2 * a_term)
        v2 = (self.total_time_s + root) / (2 * a_term)
        candidates = [v for v in (v1, v2) if v > 0]
        if not candidates:
            raise ValueError("No positive peak velocity satisfies constraints.")
        return min(candidates)

    def get_target_velocity(self, t_s):
        if t_s < 0 or t_s > self.total_time_s:
            return 0.0

        if t_s < self.t_end_acc:
            progress = t_s / self.t_acc
            return self.v_max * (1 - math.cos(math.pi * progress)) / 2

        if t_s < self.t_start_dec:
            return self.v_max

        time_in_dec = t_s - self.t_start_dec
        progress = time_in_dec / self.t_dec
        return self.v_max * (1 + math.cos(math.pi * progress)) / 2


def circular_arc_radius(chord_mm, sagitta_mm):
    if sagitta_mm <= 0:
        return float('inf')
    if sagitta_mm >= chord_mm / 2:
        raise ValueError("Sagitta too large for a single circular arc.")
    return (chord_mm ** 2) / (8 * sagitta_mm) + sagitta_mm / 2


def circular_arc_length(chord_mm, sagitta_mm):
    if sagitta_mm <= 0:
        return chord_mm
    radius = circular_arc_radius(chord_mm, sagitta_mm)
    theta = 2 * math.asin(chord_mm / (2 * radius))
    return radius * theta
