from dataclasses import dataclass, field
from uuid import UUID

@dataclass(frozen=True)
class LocationAutomationContext:
    location_id: UUID
    zone_id: UUID
    zone_name: str
    latest_moisture: float | None
    latest_light: float | None
    threshold_low: float 
    threshold_high: float
    has_moisture_sensor: bool