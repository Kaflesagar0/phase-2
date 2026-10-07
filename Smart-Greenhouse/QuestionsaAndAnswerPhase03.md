# Phase 3 — Abstract Factory questions

**Pattern / focus:** Abstract Factory.

**Read first:** [Guide 03](../../materials/guides/03-abstract-factory.md) · [Requirements](requirements.md)

## How to answer

- Use your own wording. Do not paste teaching-example types (for example warrior/mage class kits) as if they were your greenhouse classes.
- When a question asks about *this application*, refer to device families, provision, and the unified devices API from the lab.
- Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
- Write each answer inside the matching **Your Answer** note. Replace the placeholder; leave the question text unchanged.

## A. Pattern

1. State the intent of Abstract Factory in plain language. What goes wrong when related products are chosen independently (`if format` for each piece) instead of as a **family**?

> [!NOTE]
> ***Your Answer***
>
> _(The intent of the Abstract Factory is to provide an interfae for creating entire families of related or dependent objects. If we choose related products independently using if format for each piece, we will risk of broken integrations, configuration bugs, adn runtime crashes due to mixing of the incompatible components.)_

2. Name the main participants (**abstract factory**, **concrete factory**, **abstract products**, **concrete products**, **client**). How does choosing a factory at the start **commit** the client to one family?

> [!NOTE]
> ***Your Answer***
>
> _(The main participants are:-**abstract factory** Interface to create a set of related products,  **concrete factory** Implements creation of a specific family, **abstract products** Interface for a single product category, **concrete products** Family-specific implementation, **client** Uses the products without knowing their concrete classes. Choosing a factory at the start locks the client into that family and that ensures all created objects are compatible .)_

3. When should you use Abstract Factory, and when should you skip it (for example only one product type per request, or mixing siblings is valid)?

> [!NOTE]
> ***Your Answer***
>
> _(When our application needs to provision whole kit of multiple products that must together, we should use Abstract Factory. When we are creating single, independent products, then we can skip it.)_
 
## B. This phase of the application

4. In this lab, what is a **device family**, and what does `create_device_set()` (or your equivalent) return? Why must a simulation kit and an edge kit not mix incompatible siblings?

> [!NOTE]
> ***Your Answer***
>
> _(A device family defines an operational environment profile which dictates the greenhouse hardwares should behave. The `create_device_set()` returns the list of domain entities pre-configured with specific protocols and thresholds(it returns 4 in this case). Simulation kit and edge kit components rely on different values, which cannot be interchanged, so a simulation kit and an edge kit must not mix incompatable siblings.)_

5. Phase 2 Factory Method creators still exist. How does Abstract Factory **compose** them rather than replace them? What would you lose if you deleted the sensor creators and inlined all construction inside the family factory?

> [!NOTE]
> ***Your Answer***
>
> _(Abstract Factory composes by having the family factories call the sensor creators and then combines them with actuator definitions. If we deleted the sensor creators and inlined everything, we would duplicate the sensor creation logic across multiple files.)_

6. Why add a `device_family` column on the existing `devices` table (with a default/backfill such as `"simulation"`) instead of a new table per family? What happens to Phase 2 sensor rows if you forget the backfill?

> [!NOTE]
> ***Your Answer***
>
> _(Adding a column on the existing table keeps all device inventory under a single schema, and it allows us to manage sensors and actuators together. If we forget the backfill, older sensor rows will lack a family value, and it would cause query errors.)_

7. `POST /api/devices/provision` returns a kit (expected size: two sensors and two actuators). `GET /api/devices` can filter by `family` and `role`. Why must the UI be able to filter by family? Why do `/api/sensors` routes from Phase 2 still need to work?

> [!NOTE]
> ***Your Answer***
>
> _(The UI must be able to filter by family so the user can toggle between different operational environments without mixing up device kit on the dashboard. The /api/sensors routes must continue to work to make sure the backward compatibility works.)_

## C. Compare, contrast, and scenarios

8. Draw the contrast in one paragraph: Factory Method vs Abstract Factory. Use the questions “which **one** product?” versus “which product **line**?” and mention that Abstract Factory often **uses** Factory Method–style methods inside.

> [!NOTE]
> ***Your Answer***
>
> _(Factory method answers the question "which one product?" by delegating the creation of a single object type to a class or method. Abstract Factory answers "which product line?" by provisioning an entire family of related, dependent objects which belong together. To build the bundles, Abstract factory often composes and used Factory Method-style creators inside.)_

9. A DTO or HTTP handler constructs concrete simulation/edge device types directly, bypassing the family factory. What consistency bug can that reintroduce? How should HTTP stay on the abstract factory / service instead?

> [!NOTE]
> ***Your Answer***
>
> _(Bypassing the family factory reintroduces the consistency bugs where mismatched or incompatible sibling components are created. HTTP handlers could delegate all provisioning to the FamilyService adn abstract family factory, to ensure that kits are always generated as a valid bundle.)_

10. Someone proposes a single “god factory” that creates locations, readings, and devices “because we already have a factory.” Why is that a misuse of Abstract Factory?

> [!NOTE]
> ***Your Answer***
>
> _(Because it violates the Single Responsibility Principle by bundling entirely unrelated domain concepts.)_