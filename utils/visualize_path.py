import matplotlib.pyplot as plt
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
        OUTER_CAN_INSIDE_EDGE_M = 1.0
        DISTANCE_CORRECTION_M = 0.2
        MODE_STRAIGHT = "STRAIGHT"
        MODE_BONUS = "BONUS"
    config = MockConfig()

BASE_TELEMETRY_FIELDS = (
    "ms",
    "x_mm",
    "y_mm",
    "dist_mm",
    "vel_cmd",
    "heading_cmd",
    "heading_deg",
    "curvature_cmd_mm",
    "drift_dps",
)


def _is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _parse_scalar(value):
    text = value.strip()
    lower = text.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if _is_number(text):
        return float(text)
    return text

def get_bonus_path(target_dist_m, bonus_gap_m):
    target_dist_mm = (target_dist_m + config.DISTANCE_CORRECTION_M) * config.MM_PER_METER
    mid_x = target_dist_mm / 2.0
    
    # Calculate Sagitta (S) from bonus-line edge positions only.
    outer_inside_edge_m = config.OUTER_CAN_INSIDE_EDGE_M
    inside_outer_edge_m = outer_inside_edge_m - bonus_gap_m
    mid_y_m = (outer_inside_edge_m + inside_outer_edge_m) / 2.0
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


def get_straight_path(target_dist_m):
    target_dist_mm = (target_dist_m + config.DISTANCE_CORRECTION_M) * config.MM_PER_METER
    return np.array([0.0, target_dist_mm]), np.array([0.0, 0.0])

def load_telemetry(csv_path):
    """Loads recorded path and run config from a telemetry.csv file."""
    if not os.path.exists(csv_path):
        print(f"Warning: Telemetry file {csv_path} not found.")
        return None, None, {}
    
    x_coords = []
    y_coords = []
    run_info = {}
    column_indexes = {}
    
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue

                if not column_indexes and row[0].strip().lower() == "ms":
                    column_indexes = {name.strip(): idx for idx, name in enumerate(row)}
                    continue

                if not _is_number(row[0]):
                    continue

                try:
                    x_idx = column_indexes.get("x_mm", 1)
                    y_idx = column_indexes.get("y_mm", 2)

                    x_coords.append(float(row[x_idx]))
                    y_coords.append(float(row[y_idx]))
                    
                    # Store config from the first valid row
                    if not run_info:
                        if column_indexes:
                            for field, idx in column_indexes.items():
                                if field in BASE_TELEMETRY_FIELDS:
                                    continue
                                if idx < len(row):
                                    run_info[field] = _parse_scalar(row[idx])
                        elif len(row) >= 11:
                            # Legacy format: includes only target distance and bonus gap.
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
    root = None
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        root.attributes("-topmost", True)
        root.update()
        file_path = filedialog.askopenfilename(
            title="Select Telemetry CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        return file_path
    except KeyboardInterrupt:
        print("File selection interrupted. Continuing without telemetry file.")
        return None
    except tk.TclError as e:
        print(f"GUI file picker unavailable ({e}). Continuing without telemetry file.")
        return None
    finally:
        if root is not None:
            try:
                root.destroy()
            except tk.TclError:
                pass

def visualize(target_dist_m=8.0, bonus_gap_m=0.2, telemetry_path=None, run_mode=None):
    # Recorded Path (Telemetry)
    rx, ry, run_info = None, None, {}
    if telemetry_path:
        rx, ry, run_info = load_telemetry(telemetry_path)
        
        # Override defaults with info from telemetry if present
        if run_info:
            target_dist_m = float(run_info.get("target_distance_m", target_dist_m))
            bonus_gap_m = float(run_info.get("bonus_gap_m", bonus_gap_m))
            run_mode = run_info.get("mode", run_mode)
            print(f"Loaded config from telemetry: mode={run_mode}, dist={target_dist_m}m, gap={bonus_gap_m}m")

    if run_mode is None:
        run_mode = getattr(config, "MODE_STRAIGHT", "STRAIGHT")

    plt.figure(figsize=(12, 6))
    
    # Ground/Centerline
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5, label="Centerline")
    
    # Target Point (taking correction into account for the visualization of the 'stop' point)
    corrected_dist_mm = (target_dist_m + config.DISTANCE_CORRECTION_M) * config.MM_PER_METER
    plt.plot(corrected_dist_mm, 0, 'rx', markersize=10, markeredgewidth=2, label="Target Point (Corrected)")
    plt.plot(target_dist_m * config.MM_PER_METER, 0, 'ro', alpha=0.3, label="Target Point (Raw)")

    sagitta_mm = None
    if run_mode == getattr(config, "MODE_BONUS", "BONUS"):
        # Bonus gate edges (rules-defined geometry)
        mid_x_mm = corrected_dist_mm / 2.0
        outer_inside_edge_y_mm = config.OUTER_CAN_INSIDE_EDGE_M * config.MM_PER_METER
        inner_outside_edge_y_mm = outer_inside_edge_y_mm - (bonus_gap_m * config.MM_PER_METER)
        plt.plot(mid_x_mm, outer_inside_edge_y_mm, 'o', color='orange', label="Outer Can Inside Edge")
        plt.plot(mid_x_mm, inner_outside_edge_y_mm, 'o', color='brown', label="Inner Can Outside Edge")
        plt.plot(
            [mid_x_mm, mid_x_mm],
            [inner_outside_edge_y_mm, outer_inside_edge_y_mm],
            color='orange',
            linestyle=':',
            linewidth=1.5,
            label="Bonus Gap"
        )

        # Ideal bonus path
        px, py, sagitta_mm = get_bonus_path(target_dist_m, bonus_gap_m)
        plt.plot(px, py, 'b-', linewidth=2, label="Ideal Bonus Path")
    else:
        # Straight mode ideal path
        px, py = get_straight_path(target_dist_m)
        plt.plot(px, py, 'b-', linewidth=2, label="Ideal Straight Path")
    
    # Plot Recorded Path
    if rx is not None and ry is not None and len(rx) > 0 and len(ry) > 0:
        plt.plot(rx, ry, 'g--', linewidth=1.5, label="Recorded Path")
        # Mark start and end
        plt.plot(rx[0], ry[0], 'go', markersize=5, label="Start")
        plt.plot(rx[-1], ry[-1], 'rs', markersize=5, label="Stop")
    
    # Labels and Grid
    plt.title(f"Ideal vs Recorded Path (Mode: {run_mode}, Distance: {target_dist_m}m, Gap: {bonus_gap_m}m)")
    plt.xlabel("X Position (mm)")
    plt.ylabel("Y Position (mm)")
    plt.legend()
    plt.grid(True)
    plt.axis('equal') # Keep aspect ratio
    
    # Print some stats
    print(f"Run Mode: {run_mode}")
    print(f"Target Distance: {target_dist_m}m")
    print(f"Correction: {config.DISTANCE_CORRECTION_M}m")
    print(f"Effective Target: {target_dist_m + config.DISTANCE_CORRECTION_M}m")
    if sagitta_mm is not None:
        print(f"Midpoint Y (Sagitta): {sagitta_mm:.2f} mm")
    if run_info:
        print("Loaded run settings:")
        for key in sorted(run_info.keys()):
            print(f"  {key}: {run_info[key]}")
    
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize ideal and recorded vehicle paths.")
    parser.add_argument("telemetry_path", nargs="?", help="Optional telemetry CSV path. If omitted, file picker opens.")
    parser.add_argument("--distance", type=float, help="Target distance in meters")
    parser.add_argument("--gap", type=float, help="Bonus gap in meters")
    parser.add_argument("--telemetry", type=str, help="Path to telemetry CSV file (legacy flag)")
    parser.add_argument("--browse", action="store_true", help="Force file picker to select telemetry")
    
    args = parser.parse_args()
    
    # Handle telemetry path: file picker opens by default if no path is supplied.
    telemetry_path = args.telemetry_path or args.telemetry
    if args.browse or telemetry_path is None:
        selected = select_file_via_gui()
        if selected:
            telemetry_path = selected
        elif telemetry_path is None:
            print("No telemetry file selected. Showing ideal path only.")
    
    # Default values
    t_dist = 8.0
    b_gap = 0.2
    mode = getattr(config, "MODE_STRAIGHT", "STRAIGHT")
    
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
        mode = defaults.get("mode", mode)
    except:
        if args.distance: t_dist = args.distance
        if args.gap: b_gap = args.gap

    visualize(t_dist, b_gap, telemetry_path, run_mode=mode)
