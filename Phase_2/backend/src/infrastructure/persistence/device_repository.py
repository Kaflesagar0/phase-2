from sqlalchemy.orm import Session
from src.domain.sensors.entity import Sensor
from src.infrastructure.persistence.models import DeviceRow

class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_sensor(self, sensor: Sensor) -> Sensor:
        row = DeviceRow(
            device_type=sensor.device_type,
            role="sensor",
            display_name=sensor.display_name,
            default_config=sensor.default_config,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return Sensor(
            id=row.id,
            device_type=row.device_type,
            display_name=row.display_name or "",
            default_config=row.default_config,
        )

    def list_sensors(self) -> list[Sensor]:
        rows = (
            self.db.query(DeviceRow)
            .filter(DeviceRow.role == "sensor")
            .order_by(DeviceRow.created_at.desc())
            .all()
        )
        return [
            Sensor(
                id=row.id,
                device_type=row.device_type,
                display_name=row.display_name or "",
                default_config=row.default_config,
            )
            for row in rows
        ]