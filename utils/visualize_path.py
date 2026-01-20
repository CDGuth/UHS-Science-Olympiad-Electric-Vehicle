import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
import os

# Add parent directory to path so we can import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    import config
except ImportError:
    print("Warning: Could not import config.py. Using default values.")
    class MockConfig:
        MM_PER_METER = 1000.0
        CAN_DIAMETER_M = 0.075
        OUTER_CAN_INSIDE_EDGE_M = 1.0
        DISTANCE_CORRECTION_M = 0.2
    config = MockConfig()

def get_bonus_path(target_dist_m, bonus_gap_m):
    target_dist_mm = (target_dist_m + config.DISTANCE_CORRECTION_M) * config.MM_PER_METER
    mid_x = target_dist_mm / 2.0
    
    # Calculate Sagitta (S) - Y offset at cans
    r_can_m = config.CAN_DIAMETER_M / 2.0
    outer_center_m = config.OUTER_CAN_INSIDE_EDGE_M + r_can_m
    inside_outer_edge_m = config.OUTER_CAN_INSIDE_EDGE_M - bonus_gap_m
    inside_center_m = inside_outer_edge_m - r_can_m
    mid_y_m = (outer_center_m + inside_center_m) / 2.0
    sagitta_mm = mid_y_m * config.MM_PER_METER

    # Segment 1: Cosine Curve (0 to mid_x)
    x1 = np.linspace(0, mid_x, 100)
    y1 = (sagitta_mm / 2.0) * (1 - np.cos(np.pi * x1 / mid_x))

    # Segment 2: Circular Arc (mid_x to target_dist_mm)
    dx_seg2 = target_dist_mm - mid_x
    radius_mm = (dx_seg2**2 + sagitta_mm**2) / (2 * sagitta_mm)
    cent_x = mid_x
    cent_y = sagitta_mm - radius_mm
    
    x2 = np.linspace(mid_x, target_dist_mm, 100)
    # y = cy + sqrt(R^2 - (x - cx)^2)
    y2 = cent_y + np.sqrt(radius_mm**2 - (x2 - cent_x)**2)

    return np.concatenate([x1, x2]), np.concatenate([y1, y2]), sagitta_mm

def visualize(target_dist_m=8.0, bonus_gap_m=0.2):
    plt.figure(figsize=(12, 6))
    
    # Ground/Centerline
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5, label="Centerline")
    
    # Target Point (taking correction into account for the visualization of the 'stop' point)
    corrected_dist_mm = (target_dist_m + config.DISTANCE_CORRECTION_M) * config.MM_PER_METER
    plt.plot(corrected_dist_mm, 0, 'rx', markersize=10, markeredgewidth=2, label="Target Point (Corrected)")
    plt.plot(target_dist_m * config.MM_PER_METER, 0, 'ro', alpha=0.3, label="Target Point (Raw)")

    # Bonus Cans
    mid_x_mm = corrected_dist_mm / 2.0
    r_can_mm = (config.CAN_DIAMETER_M / 2.0) * config.MM_PER_METER
    outer_can_y = (config.OUTER_CAN_INSIDE_EDGE_M) * config.MM_PER_METER + r_can_mm
    inner_can_y = outer_can_y - (2 * r_can_mm + bonus_gap_m * config.MM_PER_METER)
    
    # Draw cans
    circle_outer = patches.Circle((mid_x_mm, outer_can_y), r_can_mm, color='orange', alpha=0.5, label="Outer Can")
    circle_inner = patches.Circle((mid_x_mm, inner_can_y), r_can_mm, color='orange', alpha=0.5, label="Inner Can")
    plt.gca().add_patch(circle_outer)
    plt.gca().add_patch(circle_inner)

    # Path
    px, py, S = get_bonus_path(target_dist_m, bonus_gap_m)
    plt.plot(px, py, 'b-', linewidth=2, label="Ideal Bonus Path")
    
    # Labels and Grid
    plt.title(f"Ideal Path Visualization (Distance: {target_dist_m}m, Gap: {bonus_gap_m}m)")
    plt.xlabel("X Position (mm)")
    plt.ylabel("Y Position (mm)")
    plt.legend()
    plt.grid(True)
    plt.axis('equal') # Keep aspect ratio
    
    # Print some stats
    print(f"Target Distance: {target_dist_m}m")
    print(f"Correction: {config.DISTANCE_CORRECTION_M}m")
    print(f"Effective Target: {target_dist_m + config.DISTANCE_CORRECTION_M}m")
    print(f"Midpoint Y (Sagitta): {S:.2f} mm")
    
    plt.show()

if __name__ == "__main__":
    # Default values or take from command line if you like
    t_dist = 8.0
    b_gap = 0.2
    
    # Try to grab from user_input if possible
    try:
        import user_input
        defaults = user_input.get_default_run_config()
        t_dist = defaults.get("target_distance_m", t_dist)
        b_gap = defaults.get("bonus_gap_m", b_gap)
    except:
        pass

    visualize(t_dist, b_gap)
