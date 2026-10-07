from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.infrastructure.db import get_db
from src.infrastructure.persistence.device_repository import DeviceRepository
from src.application.sensors.service import SensorService
from src.infrastructure.persistence.reading_repository import ReadingRepository
from src.infrastructure.persistence.models import DeviceRow
from src.application.readings.service import ReadingIngest

router = APIRouter(prefix="/api/sensors", tags=["Sensors & Readings"])
devices_router = APIRouter(prefix="/api/devices", tags=["Devices Sampling"])

class SamplingUpdateDto(BaseModel):
    sampling_interval_seconds: int = Field(..., ge=5)
    tracking_enabled: bool

class ReadingDto(BaseModel):
    id: UUID
    device_id: UUID
    value: float
    unit: str
    source: str
    recorded_at: str

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

#New router.get in phase 5
@router.get("/{device_id}/readings", response_model=list[ReadingDto])
def list_readings(device_id: UUID, limit: int = Query(default=10, ge=1, le=100), db: Session = Depends(get_db)):
    repo = ReadingRepository(db)
    rows = repo.list_recent(device_id, limit=limit)
    return [
        ReadingDto(
            id=r.id,
            device_id=r.device_id,
            value=float(r.value),
            unit=r.unit,
            source=r.source,
            recorded_at=r.recorded_at.isoformat(),
        )
        for r in rows
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


# New router.post in phase 5
@router.post("/{device_id}/read", response_model=ReadingDto, status_code=status.HTTP_201_CREATED)
def trigger_read(device_id: UUID, use_vendor: bool = False, db: Session = Depends(get_db)):
    try:
        service = ReadingIngest(db)
        row = service.record_one_shot(device_id, use_vendor_stub=use_vendor)
        return ReadingDto ( 
            id=row.id,
            device_id=row.device_id,
            value=float(row.value),
            unit=row.unit,
            source=row.source,
            recorded_at=row.recorded_at.isoformat(),
        )
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

@devices_router.patch("/{device_id}/sampling")
def update_sampling(device_id: UUID, payload: SamplingUpdateDto, db: Session = Depends(get_db)):
    if payload.sampling_interval_seconds < 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sampling interval must be at least 5 seconds.")

    device = db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found.")

    device.sampling_interval_seconds = payload.sampling_interval_seconds
    device.tracking_enabled = payload.tracking_enabled
    db.commit()
    db.refresh(device)

    return {
        "id": device.id,
        "sampling_interval_seconds": device.sampling_interval_seconds,
        "tracking_enabled": device.tracking_enabled,
    }