# Adapter Pattern

## Problem
In a smart greenhouse system, our domain and application layers expect a clean, normalized reading shape (`Reading` value object with `device_id`, `value`, `unit`, `source`, and `recorded_at`). However, external hardware, vendor SDKs, and inbound MQTT payloads produce widely varying raw data structures. Without the Adapter pattern, our business logic or API routers would be littered with conditional statements (`if source == ...`) to parse heterogeneous payloads, tightly coupling the core application to external formats.

## Solution
The Adapter Pattern introduces a unified domain port (`SensorPort`) and concrete adapters (`SimulationSensorAdapter`, `VendorStubSensorAdapter`, and the MQTT payload translator). Each concrete adapter implements the standard port interface, accepting its specific raw format (or generating simulation data) and translating it into the unified `Reading` value object. The application service (`ReadingIngest`) and sampler depend exclusively on the abstract port, remaining entirely agnostic of vendor-specific details.

## Code Map
- `src/domain/sensors/ports.py`: Defines the abstract `SensorPort` interface.
- `src/domain/sensors/reading.py`: Defines the pure Python `Reading` value object.
- `src/infrastructure/adapters/sensors/simulation.py`: Simulation adapter generating plausible moisture/light values within documented ranges.
- `src/infrastructure/adapters/sensors/vendor_stub.py`: Translates raw vendor-specific structures into normalized readings.
- `src/infrastructure/adapters/sensors/mqtt.py`: Translates raw MQTT dictionaries into readings without opening network sockets.
- `src/application/readings/service.py`: `ReadingIngest` service coordinating adapter selection and repository persistence.
- `src/application/readings/sampler.py`: `SimulationSampler` running background interval-based checks for tracking-enabled devices.

## Extension Exercise: Adding a Third Vendor Adapter
1. Create a new adapter class (e.g., `EcoTechSensorAdapter`) in `src/infrastructure/adapters/sensors/ecotech.py` inheriting from or implementing `SensorPort`.
2. Implement the `read(device)` method to parse EcoTech's custom raw payload format and return a normalized `Reading` with `source="ecotech"`.
3. Update the adapter factory/selector in `ReadingIngest` to recognize the new protocol or vendor flag. The database, application service, and API routes will immediately support the new sensor source without requiring modifications.