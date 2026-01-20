"""
User-editable run configuration for the EV3 vehicle.
Set USE_RUNTIME_INPUT to True to enter values on the brick before a run,
or False to use the values defined below without prompting.
"""

import config

# When True, the brick UI will collect run settings before each run (STATIC_RUN_CONFIG provides the default values).
# When False, the STATIC_RUN_CONFIG below is used directly.
USE_RUNTIME_INPUT = True

# Event level determines allowed distance increment per the rules.
# Options: "REGIONAL", "INVITATIONAL", "STATE", "NATIONAL"
EVENT_LEVEL = "STATE"

STATIC_RUN_CONFIG = {
    "mode": config.MODE_STRAIGHT,
    "target_distance_m": 7.0,
    "target_time_s": 10,
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
        return config.DISTANCE_STEP_REGIONAL_M
    if level == "STATE":
        return config.DISTANCE_STEP_STATE_M
    if level == "NATIONAL":
        return config.DISTANCE_STEP_NATIONAL_M
    return config.DISTANCE_STEP_STATE_M


def get_time_step():
    return config.TIME_STEP_S
