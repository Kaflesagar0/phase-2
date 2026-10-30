from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ActuatorContext:
    device_id: UUID
    current_state: str
    allowed_commands: list[str]