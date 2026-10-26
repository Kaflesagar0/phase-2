# Phase 7 — Facade questions

**Pattern / focus:** Facade.

**Read first:** [Guide 07](../../materials/guides/07-facade.md) · [Requirements](requirements.md)

## How to answer

- Use your own wording. Do not paste teaching-example types (for example a video publish pipeline) as if they were your greenhouse classes.
- When a question asks about _this application_, refer to the location overview, the facade, and the dashboard Overview page from the lab.
- Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
- Write each answer inside the matching **Your Answer** note. Replace the placeholder; leave the question text unchanged.

## A. Pattern

1. State the intent of Facade in plain language. What problem appears when every HTTP handler (or every UI screen) repeats the same multi-step dance across repositories and services?

> [!NOTE]
> **_Your Answer_**
>
> The Facade pattern's intent is to provide a unified, simplified interface to a complex subsystem. When every HTTP handler repeats the same multi-step dance across repositories and services, it leads to tight-coupling, duplication,and unreliable relationships.

2. A facade **orchestrates** collaborators. What should it **not** become (a god object that owns all domain logic)? Where should irrigation policy, sensor translation, and persistence stay instead?

> [!NOTE]
> **_Your Answer_**
>
>A facade mustn't house all core business logic or direct database queries. Irrigation policies stay in domain strategy an automation services, sensor translation belong in infrastructure adapters, and persistence remain in the repositories and ORM models encapsulated.

3. When should you use Facade, and when should you skip it (a single repository call is enough; or you actually need to **translate** a mismatched interface)?

> [!NOTE]
> **_Your Answer_**
>
> When a client or API endpoint needs to aggregate data from multiple subsystems, repositories, or services into a single response model, we should use a Facade. We should skip it when a simple single repository call is enough.

## B. This phase of the application

4. What does `GET /api/locations/{location_id}/overview` return? Name the main pieces of the overview DTO: location, assigned device counts, and `zones` (thresholds, assigned devices, and those devices’ latest readings, including `tracking_enabled` and `sampling_interval_seconds`), plus strategy key and last recommendation. Why may those reading rows come from the sampler or MQTT ingest, not only from `POST /read`? Why is overview scoped by `location_id`?

> [!NOTE]
> **_Your Answer_**
>
> `GET /api/locations/{location_id}/overview` returns a single unified DTO which contains location metadata, assigned device counts, a list of all zones on that location, the latest reading for each device that has one, the active strategy_key, and the computed last_recommendation. Those reading rows can also come from the sampler or MQTT ingest, because the sensor_readings table aggregates telemetry uniformly regardless of the ingestion source. Because the greenhouse domain models a location as the top-level operational container the overview is scoped by  `location_id`.

5. Why does this phase **not** require a new business table? What already exists from Phases 2–6 that the facade only **composes**?

> [!NOTE]
> **_Your Answer_**
>
> This phase does not require a new business table because it only provides a read-optimized aggregation layer for the data that is already persisted by previous phases with locations and zones, devices and sensor readings, and automation rules/strategy keys.

6. The overview HTTP handler should call **only** the facade, not reading/strategy/device repositories directly. Why? How does that help tests and later changes to the query shape?

> [!NOTE]
> **_Your Answer_**
>
> The overview HTTP handler calls only the facade to maintain the separation of concerns, which ensures that the HTTP routing logic remains clean and decoupled from multi-repository coordination. This helps tests because we can mock or unit test the facade independently of web routes, and it makes later changes to query shapes easier since modifications are encapsulated entirely within the facade and repositories.

7. The location selector may use the existing locations list. The Overview cards come from **one** overview fetch, and Refresh repeats that same fetch. Why must the React page not stitch device, reading, and automation calls together to build the same snapshot? How does a new reading or a saved strategy show up on overview without extra frontend glue?

> [!NOTE]
> **_Your Answer_**
>
> The React page must not stitch separate device, reading, and automation calls together because it would reintroduce client-side coupling, race conditions, and heavy boilerplate for managing multiple API endpoints. By fetching a single overview DTO, a new reading or saved strategy automatically appears upon refreshing or re-fetching the overview because the backend facade dynamically queries the latest database snapshot and computes recommendations on the fly.

## C. Compare, contrast, and scenarios

8. Contrast Facade with **Adapter**. One makes an existing interface usable; the other makes a subsystem simpler to call. Which is which, and how do both appear in this greenhouse app (Phase 5 vs Phase 7)?

> [!NOTE]
> **_Your Answer_**
>
> An Adapter makes an existing, incompatible interface usable by translating its shape to match a target port. A Facade makes a complex subsystem simpler to call by providing a single, unified entry point that aggregates multiple repositories and services.

9. This phase mentions **N+1** queries. What is an N+1 problem in an overview that lists latest readings for many devices, and what can the facade (or its repository) do about it without putting SQL in the router?

> [!NOTE]
> **_Your Answer_**
>
> An N+1 query problem occurs when the application executes one initial query to fetch devices, and then executes a separate database query inside a Python loop for every single device to fetch its latest reading. The repository and facade prevent this by using an efficient batch query to fetch all required latest readings in a single database round-trip, keeping SQL logic out of the router.


10. A classmate hides every error behind a generic “overview failed,” so a missing location, a DB outage, and a strategy error look the same. Why is that a trap for a facade?

> [!NOTE]
> **_Your Answer_**
>
> Hiding every error behind a generic failure is a trap because it obscures root causes, making debugging nearly impossible for clients and developers. A proper facade and its API layer should distinguish specific operational anomalies—such as returning a clean 404 Not Found for a missing location while letting valid errors surface or map appropriately, rather than masking database outages or configuration exceptions under ambiguous error codes.