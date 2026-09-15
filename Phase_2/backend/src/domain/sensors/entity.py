from dataclasses import dataclass
from uuid import UUID

@dataclass
class Sensor:
    device_type: str
    display_name: str
    default_config: dict
    id: UUID | None = None