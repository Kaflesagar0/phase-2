from datetime import datetime, timezone
from src.domain.sensors.reading import Reading

class MqttSensorAdapter:
    @staticmethod
    def translate(device_id, payload: dict) -> Reading:
        return Reading(
            device_id=device_id,
            value=float(payload["value"]),
            unit=str(payload["unit"]),
            source="mqtt",
            recorded_at=datetime.now(timezone.utc),
        )