import pytest
from src.domain.locations.config_builder import LocationConfigBuilder
from src.domain.locations.errors import ConfigurationError

def test_builder_success_path():
    builder = LocationConfigBuilder()
    builder.set_name("Greenhouse Alpha")
    builder.add_zone("Zone 1", 0.2, 0.6, {"schedule": "morning"})
    builder.add_zone("Zone 2", 0.3, 0.8)

    config = builder.build()
    assert config.location.name == "Greenhouse Alpha"
    assert len(config.location.zones) == 2
    assert config.location.zones[0].name == "Zone 1"
    assert config.location.zones[0].moisture_threshold_low == 0.2
    assert config.location.zones[0].moisture_threshold_high == 0.6

def test_builder_missing_location_name():
    builder = LocationConfigBuilder()
    builder.add_zone("Zone 1", 0.2, 0.6)
    with pytest.raises(ConfigurationError, match="Location name is required"):
        builder.build()

def test_builder_no_zones():
    builder = LocationConfigBuilder()
    builder.set_name("Empty Greenhouse")
    with pytest.raises(ConfigurationError, match="at least one zone"):
        builder.build()

def test_builder_invalid_threshold_ordering():
    builder = LocationConfigBuilder()
    builder.set_name("Bad Thresholds")
    # Low is greater than high
    builder.add_zone("Zone 1", 0.8, 0.4)
    with pytest.raises(ConfigurationError, match="strictly less than high"):
        builder.build()

def test_builder_out_of_range_vwc():
    builder = LocationConfigBuilder()
    builder.set_name("Out of Range")
    builder.add_zone("Zone 1", -0.1, 1.2)
    with pytest.raises(ConfigurationError, match="between 0.0 and 1.0"):
        builder.build()

def test_builder_duplicate_zone_names():
    builder = LocationConfigBuilder()
    builder.set_name("Duplicate Zones")
    builder.add_zone("North Wing", 0.2, 0.5)
    builder.add_zone("North Wing", 0.4, 0.7)
    with pytest.raises(ConfigurationError, match="Duplicate zone name"):
        builder.build()