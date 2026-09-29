# Phase 4 — Builder questions

**Pattern / focus:** Builder.

**Read first:** [Guide 04](../../materials/guides/04-builder.md) · [Requirements](requirements.md)

## How to answer

- Use your own wording. Do not paste teaching-example types (for example ramen orders) as if they were your greenhouse classes.
- When a question asks about _this application_, refer to locations, zones, `location_id`, and the configuration wizard from the lab.
- Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
- Write each answer inside the matching **Your Answer** note. Replace the placeholder; leave the question text unchanged.

## A. Pattern

1. State the intent of Builder in plain language. Why does construction of a complex object need **stepwise assembly** and **validation at the end** (`build()`), instead of a telescoping constructor or a half-filled dict written straight to the database?

> [!NOTE]
> **_Your Answer_**
>
> _(The intent of the Builder pattern is to separate the construction of complex object from its final representation, which allows step-by-step assembly. Stepwise assembly with a final build() validation ensures that internal invariants are fully checked and satisfied before a complete, valid domain aggregate is instantiated or persisted, while a telescoping constructor results in massive, unreadable argument lists, so the stepwise assembly and validation at the end is needed in the complex object.)_

2. Name the main participants (**product**, **builder**, **optional director**, **client**). Until `build()` succeeds, is the intermediate object a finished domain product? Why does that distinction matter?

> [!NOTE]
> **_Your Answer_**
>
> _(Product: The complex aggregate object being built.  Builder: THE interface specifying step-by-step methods to build the parts of the product. Director: Controls the construction sequence using the builder interface. CLient: THe application service/API route that initiates the builder calls and invokes build(). Until build() succeeds, the intermediate builder state is not a finished domain product.To guarantee that unvalidated, half-assembled data can never leak into the domain layer or the database, the distinction matters.)_

3. List at least three kinds of invalid configuration a location/zone `build()` should reject in **this** lab (name, zones, moisture thresholds). Why must those rules live in the **domain** builder, not only in the HTTP layer?

> [!NOTE]
> **_Your Answer_**
>
> _(The build() shoul d reject (1) missing or empty location zones. (2) locations with zero zones (3) invalid moisture threshold orderings.Because business rules and data integrity constraints are core domain responsibilities, these rules must live in the domain builder.)_

## B. This phase of the application

4. What aggregate does the builder produce (location plus zones)? Why does this course use **`location_id`** (and never `greenhouse_id`) as the name for that scope?

> [!NOTE
> **_Your Answer_**
>
> _(The builder produces a LocationConfig containing a root Location entity and a type of child Zone entities. We avoid `greenhouse_id` to maintain precise physical hierarchy terminology where a greenhouse can contain multiple distinct operational locations.)_

5. Describe the path from API request to persistence: DTO → builder steps → `build()` → repository. What must **not** be persisted if `build()` raises `ConfigurationError` (or equivalent)? Why does assigning a device wait until the zone row exists, and why does the client send only `zone_id`?

> [!NOTE]
> **_Your Answer_**
>
> _(The API receives a request DTO, passes its values into the LocationConfigBuilder steps, calls build() to validate and generate a domain configuration, and hands it to the repository for transactional saving. If build() raises a ConfigurationError, zero data must be persisted to the database. Assigning a device must wait until the zone row exists because foreign keys require a valid persistent zone.id, and the client sends only `zone_id` because the database automatically syncs `devices.location_id` from the zone.)_

6. Saving a location and its zones must be **one transaction**. What goes wrong if the location row commits and a later zone insert fails? How does that relate to “no half-built aggregates in the database”?

> [!NOTE]
> **_Your Answer_**
>
> _(If the location row commits but a subsequent zone insert fails, the database is left with an orphan location containing zero zones, which violates the core business condition that a location must have at least one zone. Treating it as a single transaction prevents partial writes, ensuring “no half-built aggregates in the database.)_

7. The configuration wizard UI collects fields in steps. How does that UI map to Builder without turning React (or the HTTP handler) into the place that owns domain validation?

> [!NOTE]
> **_Your Answer_**
>
> _(The configuration wizard UI collects user input across steps into a payload and sends it to the API, which delegates execution to the domain builder. The UI merely gathers input and displays inline error messages returned by the server; it never performs domain validation rules itself, keeping validation strictly encapsulated in the domain layer.)_

## C. Compare, contrast, and scenarios

8. Contrast Builder with Factory Method and with Abstract Factory. Which pattern answers “which type?”, which answers “which matching kit?”, and which answers “how do we assemble one **valid whole** in steps?”

> [!NOTE]
> **_Your Answer_**
>
> _(Factory method answers "which type?" by delegating the instantiation of a single item to concrete creators. Abstract factory answers “which matching kit?” by provisioning coherent families of related products (like sensors + actuators). Builder answers "how do we assemble one valid whole in steps?" by constructing complex hierarchical objects step-by-step with validation at the end.)_

9. Fluent method chaining (`builder.add_zone(...).build()`) is a coding style. Why is a fluent interface **not** the same thing as the Builder pattern?

> [!NOTE]
> **_Your Answer_**
>
> _(A fluent interface is merely a syntactic style where methods return self to allow chained dot-notation calls. While the Builder pattern often uses a fluent interface for readability, method chaining alone does not constitute a Builder pattern; a true Builder encapsulates complex construction logic and validation rules for assembling a multi-part aggregate object.)_

10. A classmate validates thresholds only in FastAPI / Pydantic and leaves `build()` empty. Another mutates builder fields after `build()` while treating the product as immutable. Explain why each is a trap.

> [!NOTE]
> **_Your Answer_**
>
> _(Validating only in Pydantic/FastAPI is a trap because it ties business logic to the web framework, leaving core domain models unprotected if instantiated outside HTTP routes. Mutating builder fields after build() while treating the product as immutable is a trap because it breaks encapsulation and thread-safety, allowing the underlying builder state to alter objects that should be fixed and frozen.)_