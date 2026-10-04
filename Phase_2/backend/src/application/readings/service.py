from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.domain.sensors.reading import Reading
from src.infrastructure.persistence.models import DeviceRow, ReadingRow
from src.infrastructure.persistence.reading_repository import ReadingRepository
from src.infrastructure.adapters.sensors.simulation import SimulationSensorAdapter
from src.infrastructure.adapters.sensors.vendor_stub import VendorStubSensorAdapter
from src.infrastructure.adapters.sensors.mqtt import MqttSensorAdapter

class ReadingIngest:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReadingRepository(db)

    def record_one_shot(self, device_id: UUID, use_vendor_stub: bool = False) -> ReadingRow:
        device = self.db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

        if use_vendor_stub:
            adapter = VendorStubSensorAdapter()
        else:
            protocol = device.default_config.get("protocol", "simulation")
            if protocol == "mqtt":
                adapter = SimulationSensorAdapter() # fallback or handled separately
            else:
                adapter = SimulationSensorAdapter()

        reading = adapter.read(device)
        return self.repo.save(reading)

    def record_translated(self, reading: Reading) -> ReadingRow:
        device = self.db.query(DeviceRow).filter(DeviceRow.id == reading.device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return self.repo.save(reading)