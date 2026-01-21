"""
Run strategies for straight and bonus modes.
Refactored to support dynamic speed adjustment and elegant path handling.
"""

import math
import config
import log_utils
from motion import circular_arc_length, circular_arc_radius

class SpeedController:
    """
    Dynamically calculates target velocity to meet time and distance goals
    while respecting physical constraints.
    """
    def __init__(self, target_distance_mm, target_time_s):
        self.target_dist_mm = target_distance_mm
        self.target_time_s = target_time_s
        self.last_time_s = 0.0
        self.last_v_mm_s = 0.0
        
        # Constraints
        self.max_v = config.MAX_SPEED_MM_S
        self.max_accel = config.MAX_ACCEL_MM_S2
        self.max_decel = config.MAX_DECEL_MM_S2
        self.creep_v = config.CREEP_SPEED_MM_S
        self.min_crawl_v = config.MIN_CRAWL_SPEED_MM_S

    def compute_target_velocity(self, time_s, dist_traveled_mm):
        """
        Calculates the optimal velocity for the current state.
        """
        dt = time_s - self.last_time_s
        self.last_time_s = time_s
        if dt <= 0:
            return self.last_v_mm_s

        dist_remaining = self.target_dist_mm - dist_traveled_mm
        time_remaining = self.target_time_s - time_s

        # 1. Determine Desired Speed based on Time
        if dist_remaining <= 0:
            v_req_time = 0.0
        elif time_remaining <= 0:
            # Time has expired, but we still have distance to cover.
            # Move at creep speed to finish accurately.
            v_req_time = self.creep_v
        else:
            # Normal operation: Try to match average speed needed
            v_req_time = dist_remaining / time_remaining

        # 2. Determine Safe Speed based on Stopping Distance
        # v^2 = 2 * a * d  =>  v = sqrt(2 * a * d)
        if dist_remaining > 0:
            v_safe_limit = math.sqrt(2 * self.max_decel * dist_remaining)
        else:
            v_safe_limit = 0.0

        # Choose the stricter of the requirements
        # If v_req_time is dangerously high compared to stopping distance, v_safe_limit takes over.
        target_v = min(v_req_time, v_safe_limit, self.max_v)

        # Ensure we don't stall if we still have far to go and time is tight
        if dist_remaining > config.TARGET_REACHED_TOLERANCE_MM and target_v < self.min_crawl_v:
             if time_remaining > 0: 
                 # If we have time, but v_req is low? (Calculated above).
                 pass
             else:
                 # Over time, force creep
                 target_v = max(target_v, self.creep_v)

        # 3. Apply Acceleration/Deceleration Limits (Rate Limiting)
        # We limit the change from the PREVIOUS COMMANDED velocity
        accel_limit = self.max_accel * dt
        decel_limit = self.max_decel * dt

        if target_v > self.last_v_mm_s:
            # Accelerating
            v_cmd = min(target_v, self.last_v_mm_s + accel_limit)
        else:
            # Decelerating
            v_cmd = max(target_v, self.last_v_mm_s - decel_limit)

        self.last_v_mm_s = v_cmd
        return v_cmd


class Path:
    """Base class for geometric paths."""
    def __init__(self, run_config):
        self.config = run_config
        self.target_dist_mm = (run_config["target_distance_m"] + config.DISTANCE_CORRECTION_M) * config.MM_PER_METER
        self._length = self.target_dist_mm

    @property
    def total_length(self):
        return self._length

    def get_lookahead_point(self, pose):
        """
        Returns (x, y) coordinates of the lookahead point based on current pose.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get_curvature(self, x):
        """Returns the curvature (kappa) at the given x coordinate."""
        return 0.0
    
    def _project_point(self, x, dist):
        """Helper to clamp x to target and return basic line projection."""
        return min(x + dist, self.target_dist_mm)


class StraightPath(Path):
    """A straight line path from (0,0) to (Target, 0)."""
    
    def get_lookahead_point(self, pose):
        x, y, _, _ = pose
        lookahead = config.LOOKAHEAD_DIST_MM
        
        # Look ahead on the X axis
        target_x = self._project_point(x, lookahead)
        target_y = 0.0 # Strict line following on Y=0
        
        return target_x, target_y


class BonusPath(Path):
    """
    Bonus run path: Cosine lane change -> Circular arc.
    """
    def __init__(self, run_config):
        super().__init__(run_config)
        self.gap_m = run_config["bonus_gap_m"]
        
        # Geometry Setup
        self.mid_x = self.target_dist_mm / 2.0
        
        # Calculate Sagitta (S)
        r_can_m = config.CAN_DIAMETER_M / 2.0
        outer_center_m = config.OUTER_CAN_INSIDE_EDGE_M + r_can_m
        inside_outer_edge_m = config.OUTER_CAN_INSIDE_EDGE_M - self.gap_m
        inside_center_m = inside_outer_edge_m - r_can_m
        mid_y_m = (outer_center_m + inside_center_m) / 2.0
        if mid_y_m <= 0:
            raise ValueError("Gap configuration invalid: Path crosses centerline.")
            
        self.sagitta_mm = mid_y_m * config.MM_PER_METER

        # Calculate Segment 2 (Arc) properties
        # Center X is MidX (tangent continuity at peak)
        dx_seg2 = self.target_dist_mm - self.mid_x
        # R = (dx^2 + S^2) / 2S
        self.radius_mm = (dx_seg2**2 + self.sagitta_mm**2) / (2 * self.sagitta_mm)
        self.cent_x = self.mid_x
        self.cent_y = self.sagitta_mm - self.radius_mm
        
        self._length = self._calculate_complex_length()

    def _calculate_complex_length(self):
        # Segment 1: Cosine Integration
        points = config.BONUS_PATH_INTEGRATION_STEPS
        len1 = 0.0
        last_x, last_y = 0.0, 0.0
        for i in range(1, points + 1):
            curr_x = (i / points) * self.mid_x
            curr_y = (self.sagitta_mm / 2.0) * (1 - math.cos(math.pi * curr_x / self.mid_x))
            dist = math.sqrt((curr_x - last_x)**2 + (curr_y - last_y)**2)
            len1 += dist
            last_x, last_y = curr_x, curr_y

        # Segment 2: Circular Arc
        dx_seg2 = self.target_dist_mm - self.mid_x
        val = dx_seg2 / self.radius_mm
        if val > 1.0: val = 1.0
        theta = math.asin(val)
        len2 = self.radius_mm * theta
        
        return len1 + len2
    def get_curvature(self, x):
        if x <= self.mid_x:
            # Segment 1: Cosine Curve
            # y = (S/2) * (1 - cos(pi * x / MidX))
            # k = pi / MidX
            # y' = (S/2) * k * sin(k*x)
            # y'' = (S/2) * k^2 * cos(k*x)
            if x < 0: x = 0
            
            k = math.pi / self.mid_x
            amp = self.sagitta_mm / 2.0
            
            yp = amp * k * math.sin(k * x)
            ypp = amp * k * k * math.cos(k * x)
            
            kappa = ypp / math.pow(1 + yp*yp, 1.5)
            return kappa
        else:
            # Segment 2: Circular Arc
            # Curve is turning Right (negative Y direction relative to tangent?)
            # Coordinate check: P1 (MidX, S) -> P2 (TargetX, 0).
            # Tangent at P1 is 0.
            # Point P2 has y < S.
            # So we are curving "down" / Right.
            # Curvature is negative.
            if x > self.target_dist_mm:
                return 0.0 # Straight after target?
            return -1.0 / self.radius_mm
    def get_lookahead_point(self, pose):
        x, y, _, _ = pose
        lookahead = config.LOOKAHEAD_DIST_MM
        
        # Project pure x-based progress for lookahead
        # (Simplification: assumes forward motion approx maps to x)
        target_x_proj = self._project_point(x, lookahead)

        if target_x_proj <= self.mid_x:
            # Segment 1: Cosine Curve
            # y = (S/2) * (1 - cos(pi * x / MidX))
            term = math.cos(math.pi * target_x_proj / self.mid_x)
            target_y = (self.sagitta_mm / 2.0) * (1 - term)
        else:
            # Segment 2: Circular Arc (Upper branch)
            # (x - cx)^2 + (y - cy)^2 = R^2
            dx = target_x_proj - self.cent_x
            
            # Check if within circle definition
            if abs(dx) > self.radius_mm:
                target_y = 0.0 # Clamp if logic fails (shouldn't if x clamped)
            else:
                # y = cy + sqrt(R^2 - dx^2)
                # Since cent_y is usually negative (S - R), and we want positive Y,
                # we add the sqrt root.
                target_y = self.cent_y + math.sqrt(self.radius_mm**2 - dx**2)

        return target_x_proj, target_y


class RunStrategy:
    """
    Orchestrates the path following and speed control.
    """
    def __init__(self, run_config):
        self.mode = run_config["mode"]
        
        # geometric path
        if self.mode == config.MODE_STRAIGHT:
            self.path = StraightPath(run_config)
        elif self.mode == config.MODE_BONUS:
            self.path = BonusPath(run_config)
        else:
            raise ValueError("Unknown Run Mode: " + str(self.mode))
            
        # dynamic speed controller
        self.speed_controller = SpeedController(
            self.path.total_length,
            run_config["target_time_s"]
        )

    @property
    def total_path_length(self):
        return self.path.total_length
    
    @property
    def target_time_s(self):
        return self.speed_controller.target_time_s

    def get_target_state(self, time_s, pose):
        """
        Calculates the instantaneous target velocity and heading.
        """
        x, y, h, d_trav = pose
        
        # 1. Update Speed Plan
        target_v = self.speed_controller.compute_target_velocity(time_s, d_trav)
        
        # 2. Update Steering Plan (Pure Pursuit)
        target_x, target_y = self.path.get_lookahead_point(pose)
        
        dx = target_x - x
        dy = target_y - y
        
        # If very close to end, strict heading 0? 
        # Or just allow pursuit to finish.
        if math.sqrt(dx*dx + dy*dy) < config.TARGET_REACHED_TOLERANCE_MM and target_x >= self.path.target_dist_mm:
            target_heading = 0.0
        else:
             # Pure Pursuit: Points the vehicle towards the lookahead point on the path.
             # If we are off-course (non-zero cross-track error), this vector naturally
             # points back towards the path, inducing a corrective turn.
             target_heading = math.degrees(math.atan2(dy, dx))
             
        # 3. Calculate Curvature Feedforward
        target_kappa = self.path.get_curvature(x)

        return target_v, target_heading, target_kappa

    def is_finished(self, time_s, pose):
        """
        Determines if the run is complete based on distance traveled.
        """
        d_trav = pose[3]
        return d_trav >= self.path.total_length


def get_strategy(run_config):
    """Factory function to create the correct strategy object."""
    return RunStrategy(run_config)
