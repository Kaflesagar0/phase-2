from uuid import UUID
from src.domain.actuators.ports import ActuatorPort

class SimulationActuatorAdapter(ActuatorPort):
    def apply(self, device_id: UUID, command: str, payload: dict) -> None:
        print(f"[SIMULATION ACTUATOR] Device {device_id} executed command '{command}' with payload {payload}")