import pytest
from src.domain.devices.family_factory import get_family_factory, SimulationDeviceFactory, EdgeDeviceFactory

def test_simulation_factory_kit():
    factory= SimulationDeviceFactory()
    devices= factory.create_device_set()

    assert len(devices) == 4
    assert all(d.device_family == "simulation" for d in devices)

    roles = [d.role for d in devices]
    assert roles.count("sensor") == 2
    assert roles.count("actuator") == 2

    water_pump = next(d for d in devices if d.device_type == "water_pump")
    assert water_pump.default_config["protocol"] == "mqtt"

    def test_edge_factory_kit():
        factory = EdgeDeviceFactory()
        devices = factory.create_device_set()

        assert len(devices) == 4
        assert all(d.device_family == "edge" for d in devices)

        water_pump  = next(d for d in devices if d.device_type == "water_pump")
        assert water_pump.default_config["protocol"] == "gpio"
        assert water_pump.default_config["pin"] == 17

    def test_family_registry_lookup():
            sim_factory = get_family_factory("simulation")
            assert isinstance(sim_factory, SimulationDeviceFactory)

            edge_factory = get_family_factory("edge")
            assert isinstance(edge_factory, EdgeDeviceFactory)

    def test_unknown_family_raises_error():
         with pytest.raises(ValueError, match="Unknown device family 'quantum'"):
              get_family_factory("quantum")