from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.infrastructure.db import get_db
from src.infrastructure.persistence.device_repository import DeviceRepository
from src.application.devices.family_service import FamilyService
from src.application.devices.dto import DeviceDto
from src.application.devices.mappers import map_device_to_dto

router = APIRouter(prefix="/api/devices", tags=["Devices"])

def get_family_service(db: Session = Depends(get_db)) -> FamilyService:
    return FamilyService(DeviceRepository(db))

@router.get("", response_model=list[DeviceDto])
def list_devices(
    family: str | None = Query(None, description="Filter by device family (simulation/edge"),
    role: str | None = Query(None, description="Filter by role (sensor/actuator)"),
    service: FamilyService = Depends(get_family_service),

):
    devices = service.list_devices(family=family, role=role)
    return [map_device_to_dto(d) for d in devices]

@router.post("/provision", response_model=list[DeviceDto], status_code=status.HTTP_201_CREATED)
def provision_family(
    family: str = Query(..., description="Device family key to provision (simulation or edge)"),
    service: FamilyService = Depends(get_family_service),
):
    try: 
        created_devices = service.provision_family(family)
        return [map_device_to_dto(d) for d in created_devices]
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err) )