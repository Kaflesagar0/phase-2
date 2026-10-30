class IllegalTransitionError(ValueError):
    """Raised when an actuator state transition violates the transition table."""
    pass

VALID_STATES = {"off", "idle", "running", "error", "maintenance"}

# Define legal transition edges and their allowed commands
TRANSITION_TABLE: dict[str, set[str]] = {
    "off": {"idle", "maintenance"},
    "idle": {"running", "off", "error", "maintenance"},
    "running": {"idle", "error", "maintenance"},
    "error": {"idle", "maintenance"},
    "maintenance": {"idle", "off"},
}

STATE_COMMANDS: dict[str, list[str]] = {
    "off": ["turn_on", "start_maintenance"],
    "idle": ["start_pump", "turn_off", "trigger_error", "start_maintenance"],
    "running": ["stop_pump", "trigger_error", "start_maintenance"],
    "error": ["reset_error", "start_maintenance"],
    "maintenance": ["end_maintenance", "turn_off"],
}

def validate_transition(current_state: str, target_state: str) -> None:
    if target_state not in VALID_STATES:
        raise IllegalTransitionError(f"Invalid target state: '{target_state}'")
    allowed_targets = TRANSITION_TABLE.get(current_state, set())
    if target_state not in allowed_targets:
        raise IllegalTransitionError(
            f"Illegal transition from '{current_state}' to '{target_state}'"
        )

def get_allowed_commands(current_state: str) -> list[str]:
    return STATE_COMMANDS.get(current_state, [])