"""Simple logging wrapper using EV3 DataLog."""

from pybricks.tools import DataLog # pyright: ignore[reportMissingImports]


class RunLogger:
    def __init__(self, target_dist_m=0.0, bonus_gap_m=0.0):
        self.target_dist_m = target_dist_m
        self.bonus_gap_m = bonus_gap_m
        self.telemetry = DataLog(
            "ms",
            "x_mm",
            "y_mm",
            "dist_mm",
            "vel_cmd",
            "heading_cmd",
            "heading_deg",
            "curvature_cmd_mm",
            "drift_dps",
            "target_dist_m",
            "bonus_gap_m",
            name="telemetry",
            timestamp=False,
        )
        self.events = DataLog("ms", "event", name="events", timestamp=False)

    def event(self, ms, message):
        self.events.log(ms, message)

    def state(self, ms, x_mm, y_mm, dist_mm, vel_cmd, heading_cmd, heading_deg, curvature_cmd_mm, drift_dps):
        self.telemetry.log(
            ms,
            x_mm,
            y_mm,
            dist_mm,
            vel_cmd,
            heading_cmd,
            heading_deg,
            curvature_cmd_mm,
            drift_dps,
            self.target_dist_m,
            self.bonus_gap_m,
        )
