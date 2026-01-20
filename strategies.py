"""Run strategies for straight and bonus modes."""

import math
import config
from motion import SCurveProfile, circular_arc_length, circular_arc_radius

class RunStrategy:
    """Base class for run strategies."""
    def __init__(self, run_config):
        self.config = run_config
        self.target_distance_m = run_config["target_distance_m"] + config.DISTANCE_CORRECTION_M
        self.target_dist_mm = self.target_distance_m * config.MM_PER_METER
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

    def get_target_state(self, time_s, pose):
        """Returns target velocity (mm/s) and heading (deg)."""
        raise NotImplementedError

    def is_finished(self, time_s):
        return time_s >= self.target_time_s

class StraightRun(RunStrategy):
    """
    Strategy for a straight line run.
    Aim at target point.
    """
    def _calculate_path_length(self):
        return self.target_dist_mm # Straight line distance

    def get_target_state(self, time_s, pose):
        x, y, h, d_trav = pose
        target_v = self.profile.get_target_velocity(time_s)
        
        # Pure Pursuit / Aim at Target
        target_x = self.target_dist_mm
        target_y = 0.0
        
        dx = target_x - x
        dy = target_y - y
        dist_to_target = math.sqrt(dx*dx + dy*dy)
        
        if dist_to_target < config.TARGET_REACHED_TOLERANCE_MM:
            target_heading = 0.0
        else:
             target_heading = math.degrees(math.atan2(dy, dx))
             
        return target_v, target_heading

class BonusRun(RunStrategy):
    """
    Bonus run composed of two segments:
    1. A cosine-interpolated lane change from Start to the Bonus Cans (Parallel to center line).
    2. A circular arc from the Bonus Cans back to the Target Point.
    """
    def __init__(self, run_config):
        self.gap_m = run_config["bonus_gap_m"]
        super().__init__(run_config)
        
        # Geometry Setup
        # P0: (0, 0)
        # P1: (MidX, S)  -- Between cans
        # P2: (TargetX, 0)
        
        self.mid_x = self.target_dist_mm / 2.0
        self.target_x = self.target_dist_mm
        
        # Calculate Sagitta (S) - Y offset at cans
        r_can_m = config.CAN_DIAMETER_M / 2.0
        outer_center_m = config.OUTER_CAN_INSIDE_EDGE_M + r_can_m
        inside_outer_edge_m = config.OUTER_CAN_INSIDE_EDGE_M - self.gap_m
        inside_center_m = inside_outer_edge_m - r_can_m
        mid_y_m = (outer_center_m + inside_center_m) / 2.0
        if mid_y_m <= 0:
            raise ValueError("Chosen gap pulls the midpoint inside the centerline; adjust bonus_gap_m.")
        self.sagitta_mm = mid_y_m * config.MM_PER_METER

        # Segment 2: Circular Arc parameters
        # From (MidX, S) with Heading 0 to (TargetX, 0).
        # Circle Center (Cx, Cy)
        # Since tangent at P1 is horizontal (heading 0), Center X must be MidX.
        # Cx = MidX
        # Circle passes through (TargetX, 0).
        # Eq: (TargetX - MidX)^2 + (0 - Cy)^2 = R^2
        # Center is at (MidX, S - R) assuming turning Right to go down.
        # Cy = S - R.
        # R = Cy - (S - R) ?? No.
        # Radius R. Center (MidX, S - R).
        # (TargetX - MidX)^2 + (0 - (S - R))^2 = R^2
        # Let dx = TargetX - MidX.
        # dx^2 + (R - S)^2 = R^2
        # dx^2 + R^2 - 2RS + S^2 = R^2
        # dx^2 + S^2 = 2RS
        # R = (dx^2 + S^2) / (2S)
        
        dx_seg2 = self.target_dist_mm - self.mid_x
        self.radius_mm = (dx_seg2**2 + self.sagitta_mm**2) / (2 * self.sagitta_mm)
        self.cent_x = self.mid_x
        self.cent_y = self.sagitta_mm - self.radius_mm
        
        # Calculate lengths
        self._precalculate_lengths()

    def _calculate_path_length(self):
        # Called by init before we have fully set up our custom geometry variables.
        # so we return a placeholder here and do real calculation in __init__ 
        # But base __init__ needs it for Profile.
        
        # We need to compute it temporarily or structured differently.
        # Re-computing sagitta here to satisfy the flow.
        
        r_can_m = config.CAN_DIAMETER_M / 2.0
        outer_center_m = config.OUTER_CAN_INSIDE_EDGE_M + r_can_m
        inside_outer_edge_m = config.OUTER_CAN_INSIDE_EDGE_M - self.gap_m
        inside_center_m = inside_outer_edge_m - r_can_m
        mid_y_m = (outer_center_m + inside_center_m) / 2.0
        sagitta_mm = mid_y_m * config.MM_PER_METER
        mid_x = self.target_dist_mm / 2.0

        # Segment 1: Cosine Curve Length
        # y = (S/2) * (1 - cos(pi * x / MidX))
        # Integrate sqrt(1 + (dy/dx)^2) dx from 0 to MidX
        # dy/dx = (S/2) * (pi/MidX) * sin(pi * x / MidX)
        points = config.BONUS_PATH_INTEGRATION_STEPS
        len1 = 0
        last_x = 0
        last_y = 0
        for i in range(1, points + 1):
            curr_x = (i / points) * mid_x
            curr_y = (sagitta_mm / 2.0) * (1 - math.cos(math.pi * curr_x / mid_x))
            dx_seg = curr_x - last_x
            dy_seg = curr_y - last_y
            dist = math.sqrt(dx_seg*dx_seg + dy_seg*dy_seg)
            len1 += dist
            last_x, last_y = curr_x, curr_y
            
        # Segment 2: Circular Arc
        # Length of arc from top (tangent 0) to intersection.
        # Angle alpha such that R * sin(alpha) = dx ? No.
        # Coordinates relative to center:
        # Start: (0, R) (local) -> Angle pi/2
        # End: (dx, S - R - 0) -> (dx, -(R-S))
        # Angle = asin(dx / R) ?
        # Center is (0, S-R). Point is (dx, 0).
        # x_rel = dx. y_rel = 0 - (S-R) = R - S.
        # Angle from vertical?
        # theta = atan2(x_rel, y_rel) = atan2(dx, R-S)
        # Arc Length = R * theta
        
        dx_seg2 = self.target_dist_mm - mid_x
        radius = (dx_seg2**2 + sagitta_mm**2) / (2 * sagitta_mm)
        # Safety for floating point
        val = dx_seg2 / radius
        if val > 1.0: val = 1.0
        
        theta = math.asin(val) 
        len2 = radius * theta
        
        return len1 + len2

    def _precalculate_lengths(self):
        # Store for internal use if needed
        pass

    def get_target_state(self, time_s, pose):
        x, y, h, d_trav = pose
        target_v = self.profile.get_target_velocity(time_s)

        lookahead = config.LOOKAHEAD_DIST_MM
        target_x_proj = x + lookahead
        if target_x_proj > self.target_dist_mm:
            target_x_proj = self.target_dist_mm

        # Determine which segment the target point is in
        if target_x_proj <= self.mid_x:
            # Segment 1: Cosine Curve
            # y = (S/2) * (1 - cos(pi * x / MidX))
            term = math.cos(math.pi * target_x_proj / self.mid_x)
            target_y_curve = (self.sagitta_mm / 2.0) * (1 - term)
        else:
            # Segment 2: Circular Arc
            # Circle: (x - cx)^2 + (y - cy)^2 = R^2
            # y = cy + sqrt(R^2 - (x - cx)^2)  (Upper branch check: cy is negative, we want y > cy generally?)
            # Wait, Center Y is S - R. R is large. Cy is negative.
            # Y values are positive (0 to S).
            # So we definitely want the upper branch (+sqrt).
            
            dx_sq = (target_x_proj - self.cent_x)**2
            if dx_sq > self.radius_mm**2:
                # Out of bounds (e.g. past target), clamp to target Y=0
                target_y_curve = 0
            else:
                target_y_curve = self.cent_y + math.sqrt(self.radius_mm**2 - dx_sq)

        # Pure Pursuit Calculation
        aim_dx = target_x_proj - x
        aim_dy = target_y_curve - y
        
        aim_dist = math.sqrt(aim_dx*aim_dx + aim_dy*aim_dy)
        if aim_dist < config.TARGET_REACHED_TOLERANCE_MM and target_x_proj >= self.target_dist_mm:
             # Ideally maintain heading 0 at the end? Or just let it finish.
             target_heading = 0 # Arrived
        else:
             target_heading = math.degrees(math.atan2(aim_dy, aim_dx))

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
