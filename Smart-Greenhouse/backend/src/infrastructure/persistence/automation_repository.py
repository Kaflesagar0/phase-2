from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.automation.context import LocationAutomationContext
from src.infrastructure.persistence.models import LocationRow, ZoneRow, DeviceRow, ReadingRow
from src.infrastructure.persistence.models import AutomationRuleRow

class AutomationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_strategy_key(self, location_id: UUID) -> str:
        rule = self.db.query(AutomationRuleRow).filter(AutomationRuleRow.location_id == location_id).first()
        return rule.strategy_key if rule else "conservative"

    def upsert_strategy_key(self, location_id: UUID, strategy_key: str) -> str:
        rule = self.db.query(AutomationRuleRow).filter(AutomationRuleRow.location_id == location_id).first()
        if rule:
            rule.strategy_key = strategy_key
        else:
            rule = AutomationRuleRow(location_id=location_id, strategy_key=strategy_key)
            self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule.strategy_key

    def load_location_contexts(self, location_id: UUID) -> list[LocationAutomationContext]:
        loc_row = self.db.query(LocationRow).filter(LocationRow.id == location_id).first()
        if not loc_row:
            return []

        contexts = []
        for zone in loc_row.zones:
            # Find sensors assigned to this zone
            assigned_devices = self.db.query(DeviceRow).filter(DeviceRow.zone_id == zone.id).all()
            
            moisture_sensor_ids = [d.id for d in assigned_devices if "moisture" in d.device_type.lower()]
            light_sensor_ids = [d.id for d in assigned_devices if "light" in d.device_type.lower()]

            latest_moisture = None
            has_moisture = len(moisture_sensor_ids) > 0

            if has_moisture:
                latest_m_row = (
                    self.db.query(ReadingRow)
                    .filter(ReadingRow.device_id.in_(moisture_sensor_ids))
                    .order_by(ReadingRow.recorded_at.desc())
                    .first()
                )
                if latest_m_row:
                    latest_moisture = float(latest_m_row.value)

            latest_light = None
            if light_sensor_ids:
                latest_l_row = (
                    self.db.query(ReadingRow)
                    .filter(ReadingRow.device_id.in_(light_sensor_ids))
                    .order_by(ReadingRow.recorded_at.desc())
                    .first()
                )
                if latest_l_row:
                    latest_light = float(latest_l_row.value)

            contexts.append(
                LocationAutomationContext(
                    location_id=location_id,
                    zone_id=zone.id,
                    zone_name=zone.name,
                    latest_moisture=latest_moisture,
                    latest_light=latest_light,
                    threshold_low=float(zone.moisture_threshold_low),
                    threshold_high=float(zone.moisture_threshold_high),
                    has_moisture_sensor=has_moisture,
                )
            )
        return contexts

    def get_rule_by_location(self, location_id: UUID) -> AutomationRuleRow | None:
        return self.db.query(AutomationRuleRow).fileter(AutomationRuleRow.location_id == location_id).first()