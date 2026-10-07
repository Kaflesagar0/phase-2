from src.domain.locations.entity import Location, Zone, LocationConfig
from src.domain.locations.errors import ConfigurationError

class LocationConfigBuilder:
    def __init__(self):
        self._name: str | None = None
        self._zones: list[Zone] = []

    def set_name(self, name: str) -> "LocationConfigBuilder":
        self._name = name.strip() if name else None
        return self

    def add_zone(
        self,
        name: str,
        moisture_threshold_low: float,
        moisture_threshold_high: float,
        schedule: dict | None = None,
    ) -> "LocationConfigBuilder":
        zone = Zone(
            name=name.strip() if name else "",
            moisture_threshold_low=moisture_threshold_low,
            moisture_threshold_high=moisture_threshold_high,
            schedule=schedule or {},
        )
        self._zones.append(zone)
        return self

    def build(self) -> LocationConfig:
        # Validation 1: Location name is required and non-empty
        if not self._name:
            raise ConfigurationError("Location name is required and cannot be empty.")

        # Validation 2: At least one zone is required
        if not self._zones:
            raise ConfigurationError("A location configuration must have at least one zone.")

        zone_names = set()
        for zone in self._zones:
            # Validation 3: Non-empty zone name
            if not zone.name:
                raise ConfigurationError("Zone name is required and cannot be empty.")

            # Validation 4: Threshold ranges constrained to 0.0 - 1.0 (VWC)
            if not (0.0 <= zone.moisture_threshold_low <= 1.0) or not (0.0 <= zone.moisture_threshold_high <= 1.0):
                raise ConfigurationError("Moisture thresholds must be between 0.0 and 1.0 (VWC).")

            # Validation 5: Low threshold strictly less than high threshold
            if zone.moisture_threshold_low >= zone.moisture_threshold_high:
                raise ConfigurationError("Moisture threshold low must be strictly less than high.")

            # Validation 6: Zone names unique within one location
            if zone.name in zone_names:
                raise ConfigurationError(f"Duplicate zone name '{zone.name}' within the same location.")
            zone_names.add(zone.name)

        location = Location(
            name=self._name,
            zones=tuple(self._zones),
        )
        return LocationConfig(location=location)