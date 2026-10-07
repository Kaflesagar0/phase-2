from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.locations.entity import Location, Zone, LocationConfig
from src.infrastructure.persistence.models import LocationRow, ZoneRow

class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_config(self, config: LocationConfig) -> LocationConfig:
        loc_domain = config.location
        
        # 1. Create LocationRow
        loc_row = LocationRow(name=loc_domain.name)
        self.db.add(loc_row)
        self.db.flush() # Flushes to generate loc_row.id

        # 2. Create ZoneRows linked to location_id
        zone_rows = []
        for z_domain in loc_domain.zones:
            z_row = ZoneRow(
                location_id=loc_row.id,
                name=z_domain.name,
                moisture_threshold_low=z_domain.moisture_threshold_low,
                moisture_threshold_high=z_domain.moisture_threshold_high,
                schedule=z_domain.schedule,
            )
            zone_rows.append(z_row)
            self.db.add(z_row)

        self.db.commit()
        self.db.refresh(loc_row)
        for z_row in zone_rows:
            self.db.refresh(z_row)

        return self._to_domain_config(loc_row)

    def get_by_id(self, location_id: UUID) -> LocationConfig | None:
        loc_row = self.db.query(LocationRow).filter(LocationRow.id == location_id).first()
        if not loc_row:
            return None
        return self._to_domain_config(loc_row)

    def list_locations(self) -> list[LocationRow]:
        return self.db.query(LocationRow).order_by(LocationRow.created_at.desc()).all()

    def delete_location(self, location_id: UUID) -> bool:
        loc_row = self.db.query(LocationRow).filter(LocationRow.id == location_id).first()
        if not loc_row:
            return False
        self.db.delete(loc_row)
        self.db.commit()
        return True

    @staticmethod
    def _to_domain_config(loc_row: LocationRow) -> LocationConfig:
        zones = tuple(
            Zone(
                id=z.id,
                location_id=z.location_id,
                name=z.name,
                moisture_threshold_low=float(z.moisture_threshold_low),
                moisture_threshold_high=float(z.moisture_threshold_high),
                schedule=z.schedule or {},
            )
            for z in loc_row.zones
        )
        location = Location(
            id=loc_row.id,
            name=loc_row.name,
            zones=zones,
        )
        return LocationConfig(location=location)