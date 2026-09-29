from uuid import UUID
from pydantic import BaseModel, Field

class ZoneRequestDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    moisture_threshold_low: float = Field(..., ge=0.0, le=1.0)
    moisture_threshold_high: float = Field(..., ge=0.0, le=1.0)
    schedule: dict | None = Field(default_factory=dict)

class LocationCreateRequestDto(BaseModel):
    location_name: str = Field(..., min_length=1, max_length=128)
    zones: list[ZoneRequestDto] = Field(..., min_length=1)

class ZoneResponseDto(BaseModel):
    id: UUID
    location_id: UUID
    name: str
    moisture_threshold_low: float
    moisture_threshold_high: float
    schedule: dict

class LocationMetadataDto(BaseModel):
    id: UUID
    name: str

class LocationConfigResponseDto(BaseModel):
    location: LocationMetadataDto
    zones: list[ZoneResponseDto]