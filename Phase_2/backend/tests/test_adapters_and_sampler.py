from datetime import datetime, timezone
import pytest
from unittest.mock import MagicMock

from src.domain.sensors.reading import Reading
from src.infrastructure.adapters.sensors.simulation import SimulationSensorAdapter
from src.infrastructure.adapters.sensors.vendor_stub import VendorStubSensorAdapter
from src.infrastructure.adapters.sensors.mqtt import MqttSensorAdapter
from src.application.readings.sampler import SimulationSampler

class MockDevice:
    def __init__(self, id, device_type, protocol="simulation", interval=300, tracking=True):
        self.id = id
        self.device_type = device_type
        self.default_config = {"protocol": protocol}
        self.sampling_interval_seconds = interval
        self.tracking_enabled = tracking

def test_simulation_adapter_ranges():
    adapter = SimulationSensorAdapter()
    
    moisture_device = MockDevice(id="123e4567-e89b-12d3-a456-426614174000", device_type="soil_moisture")
    reading = adapter.read(moisture_device)
    assert reading.source == "simulation"
    assert reading.unit == "vwc"
    assert 0.2 <= reading.value <= 0.6

    light_device = MockDevice(id="123e4567-e89b-12d3-a456-426614174001", device_type="light_sensor")
    reading_light = adapter.read(light_device)
    assert reading_light.source == "simulation"
    assert reading_light.unit == "lux"
    assert 200.0 <= reading_light.value <= 2000.0

def test_vendor_stub_adapter():
    adapter = VendorStubSensorAdapter()
    device = MockDevice(id="123e4567-e89b-12d3-a456-426614174002", device_type="custom_vendor")
    reading = adapter.read(device, {"raw_val": 550, "metric": "illumination"})
    
    assert reading.source == "vendor"
    assert reading.value == 550.0
    assert reading.unit == "lux"

def test_mqtt_adapter_no_socket():
    device_id = "123e4567-e89b-12d3-a456-426614174003"
    payload = {"value": 0.45, "unit": "vwc"}
    reading = MqttSensorAdapter.translate(device_id, payload)
    
    assert isinstance(reading, Reading)
    assert reading.source == "mqtt"
    assert reading.value == 0.45
    assert reading.unit == "vwc"

def test_sampler_run_once_records_when_elapsed():
    db_session = MagicMock()
    sampler = SimulationSampler(db_session)
    
    device = MockDevice(id="123e4567-e89b-12d3-a456-426614174004", device_type="soil_moisture", interval=60)
    
    # Mock database queries
    sampler.db.query().filter().all.return_value = [device]
    
    # No previous reading exists -> should sample
    sampler.repo.get_latest = MagicMock(return_value=None)
    sampler.repo.save = MagicMock()

    now = datetime.now(timezone.utc)
    count = sampler.run_once(now=now)

    assert count == 1
    sampler.repo.save.assert_called_once()