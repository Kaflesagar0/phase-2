from abc import ABC, abstractmethod
from src.domain.devices.entity import Device
from src.domain.devices.creators import get_sensor_creator

class DeviceFamilyFactory(ABC):
    family_key: str

    @abstractmethod
    def create_device_set(self) -> list[Device]:
        pass

class SimulationDeviceFactory(DeviceFamilyFactory):
    family_key = "simulation"

    def create_device_set(self) -> list[Device]:
        # Reuse Phase 2 creators for sensors
        moisture_sensor = get_sensor_creator("moisture").create_sensor(display_name="Simulated Soil Moisture")
        light_sensor = get_sensor_creator("light").create_sensor(display_name="Simulated Light Sensor")

        return [
            Device(
                device_type=moisture_sensor.device_type,
                role="sensor",
                device_family=self.family_key,
                display_name=moisture_sensor.display_name,
                default_config=moisture_sensor.default_config,
            ),
            Device(
                device_type=light_sensor.device_type,
                role="sensor",
                device_family=self.family_key,
                display_name=light_sensor.display_name,
                default_config=light_sensor.default_config,
            ),
            Device(
                device_type="water_pump",
                role="actuator",
                device_family=self.family_key,
                display_name="Simulated Water Pump",
                default_config={"protocol": "mqtt", "max_flow_rate_ml_min": 500, "simulated": True},
            ),
            Device(
                device_type="grow_light",
                role="actuator",
                device_family=self.family_key,
                display_name="Simulated Grow Light Panel",
                default_config={"protocol": "mqtt", "max_brightness_lumens": 5000, "simulated": True},
            ),
        ]

class EdgeDeviceFactory(DeviceFamilyFactory):
    family_key = "edge"

    def create_device_set(self) -> list[Device]:
        # Reuse Phase 2 creators for sensors, override defaults or wrap them
        moisture_sensor = get_sensor_creator("moisture").create_sensor(display_name="Edge Soil Moisture Node")
        light_sensor = get_sensor_creator("light").create_sensor(display_name="Edge Ambient Light Node")

        # Adjust configs for edge hardware stub
        moisture_config = {**moisture_sensor.default_config, "protocol": "i2c", "hardware_address": "0x48"}
        light_config = {**light_sensor.default_config, "protocol": "i2c", "hardware_address": "0x39"}

        return [
            Device(
                device_type=moisture_sensor.device_type,
                role="sensor",
                device_family=self.family_key,
                display_name=moisture_sensor.display_name,
                default_config=moisture_config,
            ),
            Device(
                device_type=light_sensor.device_type,
                role="sensor",
                device_family=self.family_key,
                display_name=light_sensor.display_name,
                default_config=light_config,
            ),
            Device(
                device_type="water_pump",
                role="actuator",
                device_family=self.family_key,
                display_name="Edge Relay Water Pump",
                default_config={"protocol": "gpio", "pin": 17, "hardware_version": "v1.2"},
            ),
            Device(
                device_type="grow_light",
                role="actuator",
                device_family=self.family_key,
                display_name="Edge PWM Grow Light",
                default_config={"protocol": "pwm", "pin": 18, "hardware_version": "v1.2"},
            ),
        ]

FAMILY_FACTORY_REGISTRY: dict[str, DeviceFamilyFactory] = {
    "simulation": SimulationDeviceFactory(),
    "edge": EdgeDeviceFactory(),
}

def get_family_factory(family_key: str) -> DeviceFamilyFactory:
    factory = FAMILY_FACTORY_REGISTRY.get(family_key.strip().lower())
    if not factory:
        valid_families = ", ".join(repr(k) for k in FAMILY_FACTORY_REGISTRY.keys())
        raise ValueError(f"Unknown device family '{family_key}'. Available families: {valid_families}")
    return factory