from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.persistence.location_repository import LocationRepository
from src.infrastructure.persistence.reading_repository import ReadingRepository
from src.infrastructure.persistence.automation_repository import AutomationRepository
from src.application.automation.services import AutomationService
from src.application.overview.dto import (
    LocationOverviewDto,
    LocationMetadataDto,
    DeviceCountDto,
    ZoneOverviewDto,
    ZoneDeviceDto,
    LatestReadingDto,
    RecommendationDto,
)

class LocationOverviewFacade:
    def __init__(self, db: Session):
        self.db = db
        self.location_repo = LocationRepository(db)
        self.reading_repo = ReadingRepository(db)
        self.automation_repo = AutomationRepository(db)
        self.automation_service = AutomationService(db)

    def get_overview(self, location_id: UUID) -> LocationOverviewDto:
        # 1. Load location and its zones via repository
        location_row = self.location_repo.get_location_with_zones(location_id)
        if not location_row:
            raise ValueError("Location not found")

        # 2. Query assigned devices via repository
        assigned_devices = self.location_repo.get_assigned_devices_for_location(location_id)

        sensor_count = sum(1 for d in assigned_devices if d.role == "sensor")
        actuator_count = sum(1 for d in assigned_devices if d.role == "actuator")
        device_ids = [d.id for d in assigned_devices]

        # 3. Query newest readings via repository (single batch query)
        newest_readings_map = self.reading_repo.get_newest_readings_for_devices(device_ids)

        # Group assigned devices by zone_id
        devices_by_zone = {}
        for d in assigned_devices:
            devices_by_zone.setdefault(d.zone_id, []).append(d)

        zones_dto = []
        for z in location_row.zones:
            z_devices = devices_by_zone.get(z.id, [])
            zone_device_dtos = [
                ZoneDeviceDto(
                    id=d.id,
                    device_type=d.device_type,
                    role=d.role,
                    display_name=d.display_name,
                )
                for d in z_devices
            ]

            latest_reading_dtos = []
            for d in z_devices:
                r = newest_readings_map.get(d.id)
                if r:
                    latest_reading_dtos.append(
                        LatestReadingDto(
                            device_id=d.id,
                            value=float(r.value),
                            unit=r.unit,
                            recorded_at=r.recorded_at,
                            tracking_enabled=d.tracking_enabled,
                            sampling_interval_seconds=d.sampling_interval_seconds,
                        )
                    )

            zones_dto.append(
                ZoneOverviewDto(
                    id=z.id,
                    name=z.name,
                    moisture_threshold_low=float(z.moisture_threshold_low),
                    moisture_threshold_high=float(z.moisture_threshold_high),
                    devices=zone_device_dtos,
                    latest_readings=latest_reading_dtos,
                )
            )

        # 4. Check saved strategy key and compute last_recommendation via service/repository
        rule_row = self.automation_repo.get_rule_by_location(location_id)
        strategy_key = rule_row.strategy_key if rule_row else None
        last_recommendation = None

        if strategy_key:
            evaluation = self.automation_service.evaluate_location(location_id)
            if evaluation.recommendations:
                target_rec = next(
                    (rec for rec in evaluation.recommendations if rec.action.lower() == "irrigate"), 
                    evaluation.recommendations[0]
                )
                last_recommendation = RecommendationDto(
                    action=target_rec.action,
                    reason=target_rec.reason,
                )

        return LocationOverviewDto(
            location=LocationMetadataDto(id=location_row.id, name=location_row.name),
            device_counts=DeviceCountDto(sensor=sensor_count, actuator=actuator_count),
            zones=zones_dto,
            strategy_key=strategy_key,
            last_recommendation=last_recommendation,
        )