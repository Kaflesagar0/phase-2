# Factory Method Pattern

## Problem
In a smart greenhouse, devices have heterogeneous attributes, operational thresholds, and configuration defaults (e.g., moisture levels in percentage vs. luminous flux in lux). Without Factory Method, API routes or application services instantiate concrete classes directly, scattering instantiation logic, unit setup, and validation across HTTP layers.

## Solution
The Factory Method pattern encapsulates object creation by defining an abstract creator interface (`SensorCreator`) declaring the creation method (`create_sensor`), implemented by concrete creators (`MoistureSensorCreator`, `LightSensorCreator`). An application registry decouples callers from concrete domain classes. Callers provide a type identifier (`moisture`, `light`) without knowing constructor details.

## Code Map
- `src/domain/sensors/entity.py`: Plain Python `Sensor` entity.
- `src/domain/sensors/creators.py`: Creator interface, concrete creators, and registry lookup (`get_sensor_creator`).
- `src/application/sensors/service.py`: Orchestrates creator lookup and repository persistence.
- `src/interfaces/api/sensors.py`: Exposes `POST /api/sensors` and handles invalid types cleanly.

## Extension Exercise: Adding a Temperature Sensor
1. Implement `TemperatureSensorCreator(SensorCreator)` in `src/domain/sensors/creators.py` with defaults like `{"unit": "celsius", "interval": 10}`.
2. Register `"temperature": TemperatureSensorCreator()` in `CREATOR_REGISTRY`.
3. The API and persistence layers will instantly support temperature sensors without route alterations.