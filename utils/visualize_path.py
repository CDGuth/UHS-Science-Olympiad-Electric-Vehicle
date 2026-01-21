import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
import os
import csv
import argparse
import tkinter as tk
from tkinter import filedialog

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

def load_telemetry(csv_path):
    """Loads recorded path and run config from a telemetry.csv file."""
    if not os.path.exists(csv_path):
        print(f"Warning: Telemetry file {csv_path} not found.")
        return None, None, {}
    
    x_coords = []
    y_coords = []
    run_info = {}
    
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or not row[0].replace('.','',1).isdigit():
                    continue
                try:
                    # ms, x_mm, y_mm, dist_mm, vel_cmd, heading_cmd, heading_deg, curvature_cmd_mm, drift_dps, target_dist_m, bonus_gap_m
                    x_coords.append(float(row[1]))
                    y_coords.append(float(row[2]))
                    
                    # Store config from the first valid row
                    if not run_info and len(row) >= 11:
                        run_info["target_distance_m"] = float(row[9])
                        run_info["bonus_gap_m"] = float(row[10])
                except (ValueError, IndexError):
                    continue
                    
        return np.array(x_coords), np.array(y_coords), run_info
    except Exception as e:
        print(f"Error reading telemetry: {e}")
        return None, None, {}

def select_file_via_gui():
    """Opens a file picker dialog to select a telemetry CSV file."""
    root = tk.Tk()
    root.withdraw() # Hide the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select Telemetry CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def visualize(target_dist_m=8.0, bonus_gap_m=0.2, telemetry_path=None):
    # Recorded Path (Telemetry)
    rx, ry, run_info = None, None, {}
    if telemetry_path:
        rx, ry, run_info = load_telemetry(telemetry_path)
        
        # Override defaults with info from telemetry if present
        if run_info:
            target_dist_m = run_info.get("target_distance_m", target_dist_m)
            bonus_gap_m = run_info.get("bonus_gap_m", bonus_gap_m)
            print(f"Loaded config from telemetry: dist={target_dist_m}m, gap={bonus_gap_m}m")

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

    # Ideal Path
    px, py, S = get_bonus_path(target_dist_m, bonus_gap_m)
    plt.plot(px, py, 'b-', linewidth=2, label="Ideal Bonus Path")
    
    # Plot Recorded Path
    if rx is not None and ry is not None and len(rx) > 0 and len(ry) > 0:
        plt.plot(rx, ry, 'g--', linewidth=1.5, label="Recorded Path")
        # Mark start and end
        plt.plot(rx[0], ry[0], 'go', markersize=5, label="Start")
        plt.plot(rx[-1], ry[-1], 'rs', markersize=5, label="Stop")
    
    # Labels and Grid
    plt.title(f"Ideal vs Recorded Path (Distance: {target_dist_m}m, Gap: {bonus_gap_m}m)")
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
    parser = argparse.ArgumentParser(description="Visualize ideal and recorded vehicle paths.")
    parser.add_argument("--distance", type=float, help="Target distance in meters")
    parser.add_argument("--gap", type=float, help="Bonus gap in meters")
    parser.add_argument("--telemetry", type=str, help="Path to telemetry CSV file")
    parser.add_argument("--browse", action="store_true", help="Open file picker to select telemetry")
    
    args = parser.parse_args()
    
    # Handle telemetry path
    telemetry_path = args.telemetry
    
    # If browse flag is set or no telemetry provided but we want to check
    if args.browse:
        telemetry_path = select_file_via_gui()
    elif not telemetry_path:
        # Check if default exists, if not, maybe prompt or just use None
        if os.path.exists("telemetry.csv"):
            telemetry_path = "telemetry.csv"
        else:
            print("No telemetry file specified. Use --telemetry <path> or --browse.")
    
    # Default values
    t_dist = 8.0
    b_gap = 0.2
    
    # Try to grab defaults from user_input if not provided via CLI
    try:
        import user_input
        defaults = user_input.get_default_run_config()
        if args.distance is None:
            t_dist = defaults.get("target_distance_m", t_dist)
        else:
            t_dist = args.distance
            
        if args.gap is None:
            b_gap = defaults.get("bonus_gap_m", b_gap)
        else:
            b_gap = args.gap
    except:
        if args.distance: t_dist = args.distance
        if args.gap: b_gap = args.gap

    visualize(t_dist, b_gap, telemetry_path)
