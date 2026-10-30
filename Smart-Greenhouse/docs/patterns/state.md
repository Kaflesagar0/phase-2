# State Pattern

## Purpose
The State pattern encapsulates actuator lifecycle states (`off`, `idle`, `running`, `error`, `maintenance`) and their transition validation rules within the domain layer, ensuring that invalid operational transitions are rejected before persistence.

## Key Design Decisions
- **Pure Domain Rules**: Transition matrices and validation logic (`validate_transition`, `get_allowed_commands`) reside entirely in `src/domain/actuators/state.py` without ORM or FastAPI dependencies.
- **Database Persistence**: Actuator lifecycle states are persisted in the `actuator_states` table keyed by `device_id`, surviving process restarts.
- **Derived Allowed Commands**: The UI and future command modules query `allowed_commands` dynamically derived from the current state.