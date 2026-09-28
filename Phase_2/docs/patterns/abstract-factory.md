# Abstract Factory Pattern

## Problem
As the greenhouse project grows, we need to provision coherent families of devices (e.g., a complete kit of matching sensors and actuators for either a cloud simulation environment or edge hardware). Each environment requires specific protocol defaults (such as MQTT for simulation vs. I2C/GPIO for edge hardware). Instantiating these mixed product lines manually across controllers or routes leads to tightly coupled, error-prone code.

## Solution
The Abstract Factory pattern provides an interface for creating families of related or dependent objects without specifying their concrete classes. We introduced a `DeviceFamilyFactory` abstract base class with concrete implementations (`SimulationDeviceFactory` and `EdgeDeviceFactory`). Each concrete factory orchestrates Phase 2 Sensor Factory Method creators along with actuator definitions to return a complete, pre-configured 4-device kit.

## Where to Look in Code
- `src/domain/devices/entity.py`: Unified domain `Device` entity supporting both sensors and actuators across families.
- `src/domain/devices/family_factory.py`: Abstract factory interface, concrete family factories, and the registry lookup (`get_family_factory`).
- `src/application/devices/family_service.py`: Application service orchestrating factory resolution and repository batch persistence.
- `src/interfaces/api/devices.py`: REST endpoints (`GET /api/devices` and `POST /api/devices/provision`).

## Why Device $\neq$ DTO
The domain layer represents pure business concepts and must remain completely decoupled from transport frameworks like FastAPI or Pydantic. Pydantic DTOs and mappers live strictly at the application/API boundary to translate database and domain models into JSON schemas for HTTP clients.

## Extension Exercise: Adding a Third Family (e.g., "industrial")
1. Create an `IndustrialDeviceFactory` implementing `DeviceFamilyFactory` with `family_key = "industrial"`.
2. Define custom protocol configurations (e.g., Modbus/Industrial bus).
3. Register the new factory in `FAMILY_FACTORY_REGISTRY`. The API and UI will instantly support provisioning industrial kits without modifying route handlers.