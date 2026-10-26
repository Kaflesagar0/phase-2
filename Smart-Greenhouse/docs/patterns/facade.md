# Facade Pattern

## Purpose
The Facade pattern provides a single, unified read API endpoint (`get_overview(location_id)`) for the dashboard overview panel. Instead of requiring HTTP routers or frontend clients to separately query locations, zones, device assignments, sensor readings, and automation rule evaluations, the facade encapsulates and coordinates all these subsystems behind a clean, read-optimized DTO model.

## Subsystems Hidden
- Location & Zone repositories
- Device assignment repository
- Sensor readings history repository
- Automation evaluation service (`AutomationService`)

## Key Design Decisions
- **Single Entry Point**: The router calls only the facade. Direct repository or automation service imports are prohibited in the overview router.
- **Stateless Recommendations**: `last_recommendation` is computed on-demand via the existing automation evaluation service whenever a strategy key is saved, avoiding redundant database persistence.
- **Query Optimization**: Assigned devices and newest readings are loaded using efficient batch queries rather than N+1 queries in Python loops.
- **No New Tables**: Existing tables (`locations`, `zones`, `devices`, `sensor_readings`, `automation_rules`) provide all required persistence without creating unnecessary schema artifacts.