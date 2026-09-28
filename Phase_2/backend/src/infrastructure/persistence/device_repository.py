from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.devices.entity import Device
from src.infrastructure.persistence.models import DeviceRow

class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_device(self, device: Device) -> Device:
        row = DeviceRow(
            device_type=device.device_type,
            role=device.role,
            device_family=device.device_family,
            display_name=device.display_name,
            default_config=device.default_config,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)

    def save_devices(self, devices: list[Device]) -> list[Device]:
        rows= [
            DeviceRow(
                device_type=d.device_type,
                role=d.role,
                device_family=d.device_family,
                display_name=d.display_name,
                default_cofig=d.default_config,
            )
            for d in devices
        ]
        self.db.add_all(rows)
        self.db.commit()
        for row in rows:
            self.db.refresh(row)
        return [self._to_domain(row) for row in rows]

    def list_devices(self, family: str | None = None, role: str | None=None) -> list[Device]:
        query = self.db.query(DeviceRow)
        if family:
            query = query.filter(DeviceRow.device_family == family.strip().lower())
        if role:
            query = query.filter(DeviceRow.role == role.strip().lower())

        rows= query.order_by(DeviceRow.created_at.desc()).all()
        return [self._to_domain(row) for row in rows]


       

    @staticmethod
    def _to_domain(row: DeviceRow) -> Device:
         return Device(
             id=row.id,
             device_type=row.device_type,
             role=row.role,
             device_family=row.device_family,
             display_name=row.display_name or "",
             default_config=row.default_config,
         )