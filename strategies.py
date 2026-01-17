"""Run strategies for straight and bonus modes."""

import math
import config
from motion import SCurveProfile, circular_arc_length, circular_arc_radius

class RunStrategy:
    """Base class for run strategies."""
    def __init__(self, run_config):
        self.config = run_config
        self.target_distance_m = run_config["target_distance_m"] + config.DISTANCE_CORRECTION_M
        self.target_dist_mm = self.target_distance_m * 1000.0
        self.target_time_s = run_config["target_time_s"]

        self.total_path_length = self._calculate_path_length()

        self.profile = SCurveProfile(
            self.total_path_length,
            self.target_time_s,
            config.MAX_ACCEL_MM_S2,
            config.MAX_DECEL_MM_S2,
            max_speed_mm_s=config.MAX_SPEED_MM_S,
        )

    def _calculate_path_length(self):
        """Override in subclasses to return total path length in mm."""
        return self.target_dist_mm

    def get_target_state(self, time_s, current_distance_mm):
        """Returns target velocity (mm/s) and heading (deg)."""
        raise NotImplementedError

    def is_finished(self, time_s):
        return time_s >= self.target_time_s

class StraightRun(RunStrategy):
    """
    Strategy for a straight line run.
    Target heading is always 0.
    """
    def _calculate_path_length(self):
        return self.target_dist_mm # Straight line distance

    def get_target_state(self, time_s, current_distance_mm):
        target_v = self.profile.get_target_velocity(time_s)
        return target_v, 0.0

class BonusRun(RunStrategy):
    """Bonus run using a single circular arc (constant curvature)."""
    def __init__(self, run_config):
        self.gap_m = run_config["bonus_gap_m"]
        super().__init__(run_config)

    def _calculate_path_length(self):
        r_can_m = config.CAN_DIAMETER_M / 2.0
        outer_center_m = config.OUTER_CAN_INSIDE_EDGE_M + r_can_m
        inside_outer_edge_m = config.OUTER_CAN_INSIDE_EDGE_M - self.gap_m
        inside_center_m = inside_outer_edge_m - r_can_m

        mid_y_m = (outer_center_m + inside_center_m) / 2.0
        if mid_y_m <= 0:
            raise ValueError("Chosen gap pulls the midpoint inside the centerline; adjust bonus_gap_m.")

        self.sagitta_mm = mid_y_m * 1000.0
        self.radius_mm = circular_arc_radius(self.target_dist_mm, self.sagitta_mm)
        return circular_arc_length(self.target_dist_mm, self.sagitta_mm)

    def get_target_state(self, time_s, current_distance_mm):
        target_v = self.profile.get_target_velocity(time_s)

        traveled = min(current_distance_mm, self.total_path_length)
        arc_angle_rad = traveled / self.radius_mm if self.radius_mm != float('inf') else 0.0
        target_heading = -math.degrees(arc_angle_rad)

        return target_v, target_heading

def get_strategy(run_config):
    """Factory function to create the correct strategy object."""
    mode = run_config["mode"]
    if mode == config.MODE_STRAIGHT:
        return StraightRun(run_config)
    elif mode == config.MODE_BONUS:
        return BonusRun(run_config)
    else:
        raise ValueError("Unknown Run Mode: " + str(mode))
