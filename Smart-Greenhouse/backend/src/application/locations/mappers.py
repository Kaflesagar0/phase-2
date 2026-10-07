from src.domain.locations.entity import LocationConfig, Location, Zone
from src.application.locations.dto import (
    LocationConfigResponseDto,
    LocationMetadataDto,
    ZoneResponseDto,
)

def map_location_config_to_dto(config: LocationConfig) -> LocationConfigResponseDto:
    loc = config.location
    if loc.id is None:
        raise ValueError("Cannot map unpersisted location to DTO (missing ID).")
    
    zone_dtos = []
    for zone in loc.zones:
        if zone.id is None or zone.location_id is None:
            raise ValueError("Cannot map unpersisted zone to DTO (missing ID or location_id).")
        zone_dtos.append(
            ZoneResponseDto(
                id=zone.id,
                location_id=zone.location_id,
                name=zone.name,
                moisture_threshold_low=zone.moisture_threshold_low,
                moisture_threshold_high=zone.moisture_threshold_high,
                schedule=zone.schedule,
            )
        )

    return LocationConfigResponseDto(
        location=LocationMetadataDto(id=loc.id, name=loc.name),
        zones=zone_dtos,
    )