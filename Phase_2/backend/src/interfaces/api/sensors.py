from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.infrastructure.db import get_db
from src.infrastructure.persistence.device_repository import DeviceRepository
from src.application.sensors.service import SensorService

router = APIRouter(prefix="/api/sensors", tags=["Sensors"])

class CreateSensorRequest(BaseModel):
    type: str
    display_name: str | None = None

class SensorResponse(BaseModel):
    id: UUID
    device_type: str
    display_name: str
    default_config: dict

def get_sensor_service(db: Session = Depends(get_db)) -> SensorService:
    return SensorService(DeviceRepository(db))

@router.get("", response_model=list[SensorResponse])
def get_sensors(service: SensorService = Depends(get_sensor_service)):
    sensors = service.list_sensors()
    return [
        SensorResponse(
            id=s.id,
            device_type=s.device_type,
            display_name=s.display_name,
            default_config=s.default_config,
        )
        for s in sensors
    ]

@router.post("", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor(payload: CreateSensorRequest, service: SensorService = Depends(get_sensor_service)):
    try:
        created = service.create_sensor(
            sensor_type=payload.type,
            display_name=payload.display_name,
        )
        return SensorResponse(
            id=created.id,
            device_type=created.device_type,
            display_name=created.display_name,
            default_config=created.default_config,
        )
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))