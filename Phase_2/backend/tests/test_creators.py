import pytest
from src.domain.sensors.creators import (
    MoistureSensorCreator,
    LightSensorCreator,
    get_sensor_creator,
)

def test_moisture_creator_defaults():
    creator = MoistureSensorCreator()
    sensor = creator.create_sensor()
    assert sensor.device_type == "moisture_sensor"
    assert "moisture_threshold_min" in sensor.default_config
    assert sensor.default_config["unit"] == "%"

def test_light_creator_defaults():
    creator = LightSensorCreator()
    sensor = creator.create_sensor()
    assert sensor.device_type == "light_sensor"
    assert "lux_threshold_min" in sensor.default_config
    assert sensor.default_config["unit"] == "lux"

def test_sensor_registry_resolves():
    moisture = get_sensor_creator("moisture")
    assert isinstance(moisture, MoistureSensorCreator)

    light = get_sensor_creator("light")
    assert isinstance(light, LightSensorCreator)

def test_sensor_registry_unknown_type():
    with pytest.raises(ValueError, match="Unknown sensor type 'temperature'"):
        get_sensor_creator("temperature")