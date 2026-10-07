from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.infrastructure.db import get_db
from src.application.locations.dto import (
    LocationCreateRequestDto,
    LocationConfigResponseDto,
    ZoneResponseDto,
    ZoneRequestDto,
)
from src.application.locations.mappers import map_location_config_to_dto
from src.application.locations.config_service import LocationConfigService
from src.application.locations.zone_assignment_service import ZoneAssignmentService
from src.domain.locations.errors import ConfigurationError

router = APIRouter(prefix="/api/locations", tags=["Locations"])
devices_router = APIRouter(prefix="/api/devices", tags=["Devices Assignment"])

class LocationListItemDto(BaseModel):
    id: UUID
    name: str

class ZoneAssignmentRequest(BaseModel):
    zone_id: UUID | None = None

def get_config_service(db: Session = Depends(get_db)) -> LocationConfigService:
    return LocationConfigService(db)

def get_assignment_service(db: Session = Depends(get_db)) -> ZoneAssignmentService:
    return ZoneAssignmentService(db)

@router.post("", response_model=LocationConfigResponseDto, status_code=status.HTTP_201_CREATED)
def create_location_config(payload: LocationCreateRequestDto, service: LocationConfigService = Depends(get_config_service)):
    try:
        zones_data = [z.model_dump() for z in payload.zones]
        config = service.create_location_config(payload.location_name, zones_data)
        return map_location_config_to_dto(config)
    except ConfigurationError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

@router.get("", response_model=list[LocationListItemDto])
def list_locations(service: LocationConfigService = Depends(get_config_service)):
    locs = service.list_locations()
    return [LocationListItemDto(id=l.id, name=l.name) for l in locs]

@router.get("/{location_id}/config", response_model=LocationConfigResponseDto)
def get_location_config(location_id: UUID, service: LocationConfigService = Depends(get_config_service)):
    config = service.get_config(location_id)
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return map_location_config_to_dto(config)

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: UUID, service: LocationConfigService = Depends(get_config_service)):
    success = service.delete_location(location_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return None

# --- Zone Management on Saved Location ---
@router.post("/{location_id}/zones", response_model=ZoneResponseDto, status_code=status.HTTP_201_CREATED)
def add_zone(location_id: UUID, payload: ZoneRequestDto, service: LocationConfigService = Depends(get_config_service)):
    try:
        z_row = service.add_zone(
            location_id,
            payload.name,
            payload.moisture_threshold_low,
            payload.moisture_threshold_high,
            payload.schedule,
        )
        return ZoneResponseDto(
            id=z_row.id,
            location_id=z_row.location_id,
            name=z_row.name,
            moisture_threshold_low=float(z_row.moisture_threshold_low),
            moisture_threshold_high=float(z_row.moisture_threshold_high),
            schedule=z_row.schedule,
        )
    except ConfigurationError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

@router.patch("/{location_id}/zones/{zone_id}", response_model=ZoneResponseDto)
def edit_zone(location_id: UUID, zone_id: UUID, payload: ZoneRequestDto, service: LocationConfigService = Depends(get_config_service)):
    try:
        z_row = service.edit_zone(
            location_id,
            zone_id,
            payload.name,
            payload.moisture_threshold_low,
            payload.moisture_threshold_high,
            payload.schedule,
        )
        return ZoneResponseDto(
            id=z_row.id,
            location_id=z_row.location_id,
            name=z_row.name,
            moisture_threshold_low=float(z_row.moisture_threshold_low),
            moisture_threshold_high=float(z_row.moisture_threshold_high),
            schedule=z_row.schedule,
        )
    except ConfigurationError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

@router.delete("/{location_id}/zones/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zone(location_id: UUID, zone_id: UUID, service: LocationConfigService = Depends(get_config_service)):
    try:
        service.delete_zone(location_id, zone_id)
        return None
    except ConfigurationError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

@router.get("/{location_id}/zones/{zone_id}/devices")
def list_zone_devices(location_id: UUID, zone_id: UUID, service: ZoneAssignmentService = Depends(get_assignment_service)):
    try:
        devices = service.list_devices_in_zone(location_id, zone_id)
        return [
            {
                "id": d.id,
                "device_type": d.device_type,
                "role": d.role,
                "display_name": d.display_name,
                "zone_id": d.zone_id,
                "location_id": d.location_id,
            }
            for d in devices
        ]
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

# --- Device Zone Assignment Route ---
@devices_router.patch("/{device_id}/zone")
def assign_device_zone(device_id: UUID, payload: ZoneAssignmentRequest, service: ZoneAssignmentService = Depends(get_assignment_service)):
    try:
        d = service.assign_device_zone(device_id, payload.zone_id)
        return {
            "id": d.id,
            "zone_id": d.zone_id,
            "location_id": d.location_id,
        }
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))