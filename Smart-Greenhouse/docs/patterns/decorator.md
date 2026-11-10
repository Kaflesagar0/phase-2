# Decorator Pattern

## Purpose
The **Decorator Pattern** wraps the core `ActuatorPort` adapter (`SimulationActuatorAdapter`) with transparent policy wrappers (`LoggingActuatorDecorator` and `MaxRunTimeActuatorDecorator`) without modifying the underlying adapter or requiring callers to know how many wrappers are stacked.

## Key Design Decisions
- **Shared Interface**: Both decorators and the core adapter implement the identical `ActuatorPort` interface (`apply`), ensuring complete polymorphism and transparency.
- **Composition Order**: Logging acts as the outermost decorator to guarantee attempt recording across all calls, followed by the max-run-time policy decorator, which intercepts and rejects execution before reaching the innermost simulation adapter if run time exceeds 30 minutes.
- **Persistent Execution Logs**: Every execution attempt (successful or blocked) writes a structured audit row to the `actuator_execution_log` table containing boolean success status, applied policy lists, and diagnostic messages.