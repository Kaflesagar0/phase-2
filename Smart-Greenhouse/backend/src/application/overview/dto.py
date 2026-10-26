from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class LocationMetadataDto(BaseModel):
    id: UUID
    name: str

class DeviceCountDto(BaseModel):
    sensor:int
    actuator: int

class ZoneDeviceDto(BaseModel):
    id: UUID
    device_type: str
    role: str
    display_name: str | None = None

class LatestReadingDto(BaseModel):
    device_id: UUID
    value: float
    unit: str
    recorded_at: datetime
    tracking_enabled: bool
    sampling_interval_seconds: int

class ZoneOverviewDto(BaseModel):
    id: UUID
    name: str
    moisture_threshold_low: float
    moisture_threshold_high: float 
    devices: list[ZoneDeviceDto]
    latest_readings: list[LatestReadingDto]


class RecommendationDto(BaseModel):
    action: str
    reason: str

class LocationOverviewDto(BaseModel):
    location: LocationMetadataDto
    device_counts: DeviceCountDto
    zones: list[ZoneOverviewDto]
    strategy_key: str | None = None
    last_recommendation: RecommendationDto | None = None 