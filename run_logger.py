"""Simple logging wrapper using EV3 DataLog."""

from pybricks.tools import DataLog # pyright: ignore[reportMissingImports]


class RunLogger:
    def __init__(self, run_settings=None):
        self.run_settings = dict(run_settings or {})
        self.run_setting_keys = tuple(self.run_settings.keys())
        self.run_setting_values = tuple(self.run_settings[k] for k in self.run_setting_keys)

        telemetry_headers = [
            "ms",
            "x_mm",
            "y_mm",
            "dist_mm",
            "vel_cmd",
            "heading_cmd",
            "heading_deg",
            "curvature_cmd_mm",
            "drift_dps",
        ]
        telemetry_headers.extend(self.run_setting_keys)

        self.telemetry = DataLog(
            *telemetry_headers,
            name="telemetry",
            timestamp=False,
        )
        self.events = DataLog("ms", "event", name="events", timestamp=False)

    def event(self, ms, message):
        self.events.log(ms, message)

    def state(self, ms, x_mm, y_mm, dist_mm, vel_cmd, heading_cmd, heading_deg, curvature_cmd_mm, drift_dps):
        values = [
            ms,
            x_mm,
            y_mm,
            dist_mm,
            vel_cmd,
            heading_cmd,
            heading_deg,
            curvature_cmd_mm,
            drift_dps,
        ]
        values.extend(self.run_setting_values)
        self.telemetry.log(*values)
