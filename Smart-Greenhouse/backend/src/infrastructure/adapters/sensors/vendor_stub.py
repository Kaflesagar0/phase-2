from datetime import datetime, timezone
from src.domain.sensors.ports import SensorPort
from src.domain.sensors.reading import Reading

class VendorStubSensorAdapter(SensorPort):
    def read(self, device, raw_payload: dict  | None = None ) -> Reading:
        payload= raw_payload or {"raw_val": 450, "metric": "illumination"}
        val = float(payload.get("raw_val", 0))
        unit = "lux" if "illumination" in payload.get("metric", "") else "vwc"

        return Reading(
            device_id=device.id,
            value=val,
            unit=unit,
            source="vendor",
            recorded_at=datetime.now(timezone.utc),
        )