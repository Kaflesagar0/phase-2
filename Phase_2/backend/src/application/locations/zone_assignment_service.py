from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.persistence.models import DeviceRow, ZoneRow

class ZoneAssignmentService:
    def __init__(self, db: Session):
        self.db = db

    def assign_device_zone(self, device_id: UUID, zone_id: UUID | None) -> DeviceRow:
        device_row = self.db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
        if not device_row:
            raise ValueError("Device not found.")

        if zone_id is None:
            device_row.zone_id = None
            device_row.location_id = None
        else:
            zone_row = self.db.query(ZoneRow).filter(ZoneRow.id == zone_id).first()
            if not zone_row:
                raise ValueError("Zone not found.")
            device_row.zone_id = zone_row.id
            device_row.location_id = zone_row.location_id

        self.db.commit()
        self.db.refresh(device_row)
        return device_row

    def list_devices_in_zone(self, location_id: UUID, zone_id: UUID) -> list[DeviceRow]:
        zone_row = self.db.query(ZoneRow).filter(ZoneRow.id == zone_id, ZoneRow.location_id == location_id).first()
        if not zone_row:
            raise ValueError("Zone not found or does not belong to this location.")
        
        return self.db.query(DeviceRow).filter(DeviceRow.zone_id == zone_id).all()