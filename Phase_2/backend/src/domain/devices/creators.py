from abc import ABC, abstractmethod
from src.domain.devices.entity import Sensor

class SensorCreator(ABC):
    @abstractmethod
    def create_sensor(self, display_name: str | None = None) -> Sensor:
        pass

class MoistureSensorCreator(SensorCreator):
    def create_sensor(self, display_name: str | None = None) -> Sensor:
        return Sensor(
            device_type="moisture_sensor",
            display_name=display_name or "Soil Moisture Sensor",
            default_config={
                "unit": "%",
                "sampling_interval_seconds": 60,
                "moisture_threshold_min": 30.0,
                "moisture_threshold_max": 75.0,
            },
        )

class LightSensorCreator(SensorCreator):
    def create_sensor(self, display_name: str | None = None) -> Sensor:
        return Sensor(
            device_type="light_sensor",
            display_name=display_name or "Ambient Light Sensor",
            default_config={
                "unit": "lux",
                "sampling_interval_seconds": 30,
                "lux_threshold_min": 200,
                "lux_threshold_max": 10000,
            },
        )

CREATOR_REGISTRY: dict[str, SensorCreator] = {
    "moisture": MoistureSensorCreator(),
    "light": LightSensorCreator(),
}

def get_sensor_creator(sensor_type: str) -> SensorCreator:
    creator = CREATOR_REGISTRY.get(sensor_type.strip().lower())
    if not creator:
        valid = ", ".join(repr(k) for k in CREATOR_REGISTRY.keys())
        raise ValueError(f"Unknown sensor type '{sensor_type}'. Available types: {valid}")
    return creator