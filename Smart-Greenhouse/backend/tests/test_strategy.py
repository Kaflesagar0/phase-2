import pytest
from uuid import uuid4
from src.domain.automation.context import LocationAutomationContext
from src.domain.automation.strategy import (
    get_strategy,
    ConservativeMoistureStrategy,
    AggressiveMoistureStrategy,
)

def test_get_strategy_lookup():
    assert isinstance(get_strategy("conservative"), ConservativeMoistureStrategy)
    assert isinstance(get_strategy("AGGRESSIVE"), AggressiveMoistureStrategy)
    
    with pytest.raises(ValueError, match="Unknown strategy key"):
        get_strategy("unknown_strategy")

def test_conservative_strategy_decision():
    strategy = ConservativeMoistureStrategy()
    loc_id = uuid4()
    zone_id = uuid4()

    # Context where moisture is well above low threshold (0.4 vs low 0.3) -> should wait
    ctx_safe = LocationAutomationContext(
        location_id=loc_id,
        zone_id=zone_id,
        zone_name="Zone A",
        latest_moisture=0.4,
        latest_light=500.0,
        threshold_low=0.3,
        threshold_high=0.7,
        has_moisture_sensor=True,
    )
    rec = strategy.decide(ctx_safe)
    assert rec.action == "wait"

    # Context where moisture drops below conservative trigger limit (0.3 * 0.9 = 0.27 -> reading is 0.25) -> should irrigate
    ctx_low = LocationAutomationContext(
        location_id=loc_id,
        zone_id=zone_id,
        zone_name="Zone A",
        latest_moisture=0.25,
        latest_light=500.0,
        threshold_low=0.3,
        threshold_high=0.7,
        has_moisture_sensor=True,
    )
    rec_low = strategy.decide(ctx_low)
    assert rec_low.action == "irrigate"

def test_aggressive_strategy_decision():
    strategy = AggressiveMoistureStrategy()
    loc_id = uuid4()
    zone_id = uuid4()

    # Context where moisture is right at the low threshold (0.3) -> aggressive triggers immediately
    ctx_threshold = LocationAutomationContext(
        location_id=loc_id,
        zone_id=zone_id,
        zone_name="Zone B",
        latest_moisture=0.3,
        latest_light=500.0,
        threshold_low=0.3,
        threshold_high=0.7,
        has_moisture_sensor=True,
    )
    rec = strategy.decide(ctx_threshold)
    assert rec.action == "irrigate"

def test_missing_sensor_handling():
    strategy = ConservativeMoistureStrategy()
    loc_id = uuid4()
    zone_id = uuid4()

    ctx_no_sensor = LocationAutomationContext(
        location_id=loc_id,
        zone_id=zone_id,
        zone_name="Zone C",
        latest_moisture=None,
        latest_light=None,
        threshold_low=0.3,
        threshold_high=0.7,
        has_moisture_sensor=False,
    )
    rec = strategy.decide(ctx_no_sensor)
    assert rec.action == "wait"
    assert "No moisture sensor assigned" in rec.reason