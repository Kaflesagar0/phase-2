from dataclasses import dataclass, field
from uuid import UUID

@dataclass(frozen=True)
class Device:
    device_type: str    
    display_name: str
    device_family: str = "simulation"
    role: str ="sensor"
    default_config: dict = field(default_factory=dict)
    id: UUID | None = None

Sensor = Device 