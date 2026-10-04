from datetime import datetime, timezone
import random
from uuid import UUID
from src.domain.sensors.ports import SensorPort
from src.domain.sensors.reading import Reading

class SimulationSensorAdapter(SensorPort):
    def read(self, device) -> Reading:
        dtype = device.device_type.lower()
        if "moisture" in dtype: 
            val = round(random.uniform(0.2, 0.6), 4)
            unit = "vwc"
        else: 
            val = round(random.uniform(200.0, 2000.0), 2)
            unit = "lux"

        return Reading(
            device_id=device.id,
            value=val,
            unit=unit,
            source="simulation",
            recorded_at=datetime.now(timezone.utc),
        )
