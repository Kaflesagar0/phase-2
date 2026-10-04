from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.infrastructure.persistence.models import DeviceRow
from src.infrastructure.persistence.reading_repository import ReadingRepository
from src.infrastructure.adapters.sensors.simulation import SimulationSensorAdapter

class SimulationSampler:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReadingRepository(db)
        self.adapter = SimulationSensorAdapter()

    def run_once(self, now: datetime | None = None) -> int:
        current_time = now or datetime.now(timezone.utc)
        
        # Load simulation devices with tracking enabled
        devices = (
            self.db.query(DeviceRow)
            .filter(
                DeviceRow.role == "sensor",
                DeviceRow.tracking_enabled == True,
            )
            .all()
        )

        recorded_count = 0
        for device in devices:
            protocol = device.default_config.get("protocol", "simulation")
            if protocol != "simulation":
                continue  # Skip non-simulation devices (like MQTT)

            latest_reading = self.repo.get_latest(device.id)
            interval = device.sampling_interval_seconds or 300

            should_sample = False
            if not latest_reading:
                should_sample = True
            else:
                elapsed = (current_time - latest_reading.recorded_at).total_seconds()
                if elapsed >= interval:
                    should_sample = True

            if should_sample:
                reading = self.adapter.read(device)
                self.repo.save(reading)
                recorded_count += 1

        return recorded_count