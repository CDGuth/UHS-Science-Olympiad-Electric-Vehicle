"""Simple logging wrapper using EV3 DataLog."""

from pybricks.tools import DataLog # pyright: ignore[reportMissingImports]


class RunLogger:
    def __init__(self):
        self.telemetry = DataLog(
            "ms",
            "dist_mm",
            "vel_cmd",
            "heading_cmd",
            "heading_deg",
            "drift_dps",
            name="telemetry",
            timestamp=False,
        )
        self.events = DataLog("ms", "event", name="events", timestamp=False)

    def event(self, ms, message):
        self.events.log(ms, message)

    def state(self, ms, dist_mm, vel_cmd, heading_cmd, heading_deg, drift_dps):
        self.telemetry.log(ms, dist_mm, vel_cmd, heading_cmd, heading_deg, drift_dps)
