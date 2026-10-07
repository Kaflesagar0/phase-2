# Builder Pattern in Smart Greenhouse

## Intent in this Project
The **Builder Pattern** is used in Phase 4 to construct complex `LocationConfig` aggregate objects (consisting of a location name and a tuple of child `Zone` entities) step-by-step through method chaining (`set_name`, `add_zone`), separating object construction logic from its external representation and database persistence.

## Why Builder (not Factory Method / Abstract Factory)?
- **Factory Method** (Phase 2) focuses on instantiating single heterogeneous objects (like individual sensors) by delegating to type-specific creators.
- **Abstract Factory** (Phase 3) provisions coherent multi-product families or device kits (sensors + actuators) sharing an environment family key.
- **Builder** is chosen here because a Location configuration represents a hierarchical tree structure with variable lists of child components (zones) that require complex multi-step validation rules before an unvalidated or incomplete object can be instantiated or persisted.

## Where Validation Lives
All structural and business validation rules—such as:
- Location name required and non-empty
- At least one zone required
- Non-empty zone names
- VWC moisture thresholds constrained between `0.0` and `1.0`
- Low threshold strictly less than high threshold (`low < high`)
- Unique zone names within a single location

are enforced strictly inside the domain-layer `LocationConfigBuilder.build()` method. This keeps business logic pure, highly testable, and completely independent of HTTP frameworks, Pydantic DTOs, or SQLAlchemy database sessions.

## Why `location_id` Naming is Used
To maintain architectural consistency across relational tables and APIs, `location_id` is used as the foreign key identifier in zones and related records. A device belongs to at most one zone (`devices.zone_id`), and upon assignment, `devices.location_id` is automatically populated from the zone's `location_id` within the same transactional write.

## Why Device Assignment is Not a Builder Method
Devices already exist independently (provisioned in Phases 2 and 3), and zones do not possess database IDs until the location configuration is successfully built and persisted. Therefore, device assignment is handled post-persistence through a separate dedicated `ZoneAssignmentService`, rather than coupling device attachment inside the `LocationConfigBuilder`.