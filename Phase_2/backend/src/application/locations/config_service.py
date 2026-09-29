from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.locations.config_builder import LocationConfigBuilder
from src.domain.locations.entity import LocationConfig, Zone
from src.domain.locations.errors import ConfigurationError
from src.infrastructure.persistence.location_repository import LocationRepository
from src.infrastructure.persistence.models import LocationRow, ZoneRow

class LocationConfigService:
    def __init__(self, db: Session):
        self.repository = LocationRepository(db)
        self.db = db

    def create_location_config(self, location_name: str, zones_data: list[dict]) -> LocationConfig:
        builder = LocationConfigBuilder().set_name(location_name)
        for z in zones_data:
            builder.add_zone(
                name=z["name"],
                moisture_threshold_low=z["moisture_threshold_low"],
                moisture_threshold_high=z["moisture_threshold_high"],
                schedule=z.get("schedule", {}),
            )
        config = builder.build()
        return self.repository.save_config(config)

    def get_config(self, location_id: UUID) -> LocationConfig | None:
        return self.repository.get_by_id(location_id)

    def list_locations(self) -> list[LocationRow]:
        return self.repository.list_locations()

    def delete_location(self, location_id: UUID) -> bool:
        
        return self.repository.delete_location(location_id)

    def add_zone(self, location_id: UUID, name: str, low: float, high: float, schedule: dict | None = None) -> ZoneRow:
        # Re-use builder or direct validation rules: non-empty name, thresholds 0-1, low < high, unique in location
        name_clean = name.strip() if name else ""
        if not name_clean:
            raise ConfigurationError("Zone name is required and cannot be empty.")
        if not (0.0 <= low <= 1.0) or not (0.0 <= high <= 1.0):
            raise ConfigurationError("Moisture thresholds must be between 0.0 and 1.0 (VWC).")
        if low >= high:
            raise ConfigurationError("Moisture threshold low must be strictly less than high.")

        loc_row = self.db.query(LocationRow).filter(LocationRow.id == location_id).first()
        if not loc_row:
            raise ValueError("Location not found.")

        # Check unique zone name within location
        for z in loc_row.zones:
            if z.name == name_clean:
                raise ConfigurationError(f"Duplicate zone name '{name_clean}' within the same location.")

        zone_row = ZoneRow(
            location_id=location_id,
            name=name_clean,
            moisture_threshold_low=low,
            moisture_threshold_high=high,
            schedule=schedule or {},
        )
        self.db.add(zone_row)
        self.db.commit()
        self.db.refresh(zone_row)
        return zone_row

    def edit_zone(self, location_id: UUID, zone_id: UUID, name: str, low: float, high: float, schedule: dict | None = None) -> ZoneRow:
        name_clean = name.strip() if name else ""
        if not name_clean:
            raise ConfigurationError("Zone name is required and cannot be empty.")
        if not (0.0 <= low <= 1.0) or not (0.0 <= high <= 1.0):
            raise ConfigurationError("Moisture thresholds must be between 0.0 and 1.0 (VWC).")
        if low >= high:
            raise ConfigurationError("Moisture threshold low must be strictly less than high.")

        zone_row = self.db.query(ZoneRow).filter(ZoneRow.id == zone_id, ZoneRow.location_id == location_id).first()
        if not zone_row:
            raise ValueError("Zone not found or does not belong to this location.")

        # Check unique name clash in same location excluding current zone
        loc_row = self.db.query(LocationRow).filter(LocationRow.id == location_id).first()
        for z in loc_row.zones:
            if z.id != zone_id and z.name == name_clean:
                raise ConfigurationError(f"Duplicate zone name '{name_clean}' within the same location.")

        zone_row.name = name_clean
        zone_row.moisture_threshold_low = low
        zone_row.moisture_threshold_high = high
        if schedule is not None:
            zone_row.schedule = schedule

        self.db.commit()
        self.db.refresh(zone_row)
        return zone_row

    def delete_zone(self, location_id: UUID, zone_id: UUID) -> bool:
        loc_row = self.db.query(LocationRow).filter(LocationRow.id == location_id).first()
        if not loc_row:
            raise ValueError("Location not found.")
        
        if len(loc_row.zones) <= 1:
            raise ConfigurationError("Cannot delete the last remaining zone on a location.")

        zone_row = self.db.query(ZoneRow).filter(ZoneRow.id == zone_id, ZoneRow.location_id == location_id).first()
        if not zone_row:
            raise ValueError("Zone not found.")

        # Clear devices assigned to this zone before deletion
        from src.infrastructure.persistence.models import DeviceRow
        devices = self.db.query(DeviceRow).filter(DeviceRow.zone_id == zone_id).all()
        for d in devices:
            d.zone_id = None
            d.location_id = None

        self.db.delete(zone_row)
        self.db.commit()
        return True