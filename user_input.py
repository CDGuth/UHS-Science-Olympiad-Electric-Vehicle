"""
User-editable run configuration for the EV3 vehicle.
Set USE_RUNTIME_INPUT to True to enter values on the brick before a run,
or False to use the values defined below without prompting.
"""

import config

# When True, the brick UI will collect run settings before each run.
# When False, the STATIC_RUN_CONFIG below is used directly.
USE_RUNTIME_INPUT = True

# Event level determines allowed distance increment per rules.
# Options: "REGIONAL", "INVITATIONAL", "STATE", "NATIONAL"
EVENT_LEVEL = "INVITATIONAL"

STATIC_RUN_CONFIG = {
    "mode": config.MODE_STRAIGHT,
    "target_distance_m": 1.0,
    "target_time_s": 4.0,
    # Distance between outer can inside edge (at 1.0 m) and inside can outside edge (0.0-1.0 m range)
    "bonus_gap_m": 1.0,
}


def get_default_run_config():
    """
    Returns a shallow copy of the static run configuration so callers can
    mutate values without affecting the stored defaults.
    """
    return dict(STATIC_RUN_CONFIG)


def get_distance_step():
    level = EVENT_LEVEL.upper()
    if level in ("REGIONAL", "INVITATIONAL"):
        return 0.25
    if level == "STATE":
        return 0.10
    if level == "NATIONAL":
        return 0.01
    return 0.10


def get_time_step():
    return 0.10
