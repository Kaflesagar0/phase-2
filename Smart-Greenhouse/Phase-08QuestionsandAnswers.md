# Phase 8 — State questions

**Pattern / focus:** State.

**Read first:** [Guide 08](../../materials/guides/08-state.md) · [Requirements](requirements.md)

## How to answer

- Use your own wording. Do not paste teaching-example types (for example support-ticket states) as if they were your greenhouse classes.
- When a question asks about *this application*, refer to actuator lifecycle, persisted state, and `allowed_commands` from the lab.
- Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
- Write each answer inside the matching **Your Answer** note. Replace the placeholder; leave the question text unchanged.

## A. Pattern

1. State the intent of the State pattern in plain language. What problem appears when lifecycle is modelled as boolean flags and scattered `if` guards?

> [!NOTE]
> ***Your Answer***
>
> The intent of the State pattern is to allow an object to alter its behavior when its internal state changes, encapsulating state-specific rules into dedicated classes or transition tables. When lifecycle modes are modeled as raw boolean flags (like is_running, is_fault) paired with scattered if/else conditional checks across routers and services, the codebase becomes brittle and hard to maintain. Adding a new operational state or modifying a transition rule requires hunting down and modifying conditional statements everywhere, drastically increasing the risk of illegal states and bugs.

2. Name the participants (**context**, **state interface**, **concrete states**, **client**). How does a successful command lead to a **transition**, and where do **guards** live?

> [!NOTE]
> ***Your Answer***
>
> Context: Maintains the current state reference and delegates state-dependent actions. State Interface: Defines the legal edges and allowed actions for each operational mode. Concrete States: Encapsulate the behaviour and rules associated with specific lifecycle states. Client: Triggers the action or command.   A successful command passes through the domain guard validator to verify that the target transition is permitted by the transition table before updating the database. Guards live in the domain layer.

3. What is `allowed_commands` (or equivalent) for? Why is exposing “what can I do **now**?” better than letting the UI guess from a raw state string?

> [!NOTE]
> ***Your Answer***
>
> allowed_commands is a dynamically derived list of legal command names valid for an actuator's current state. Because exposing "what can I do now?" centralizes business logic in the backend, prevents the frontend from duplicating transition rules, and ensures the user interface only diplays valid operational controls, it is better than letting UI guess from a raw state string.

## B. This phase of the application

4. Which actuator states did you implement (for example idle, running, error)? Sketch the **legal** transitions (which command or event moves idle → running, running → idle, into error, and out of error).

> [!NOTE]
> ***Your Answer***
>
> We implemented five core actuator lifecycle states: off, idle, running, error, and maintenance.
>off --> idle or maintenance
>idle --> running, off, error, or maintenance
>running --> idle, error, or maintenance
>error --> idle or maintenance
>maintenance --> idle or off

5. Why is actuator state stored in `actuator_states` (or equivalent) rather than only in process memory? What must still be true after you restart the backend?

> [!NOTE]
> ***Your Answer***
>
>Actuator state is stored in the persistent actuator_states database table rather than in process memory so that operational states survive backend service restarts, container reboots, and deployments. After restarting the backend, an actuator's last recorded state and its corresponding allowed_commands must still be accurately loaded from the database without defaulting back to an uninitialized state.

6. An **illegal** transition must raise a domain error and **must not** update the database. Why? Which HTTP status is reasonable for that case (400 or 409), and why should the rule live in the domain rather than in React?

> [!NOTE]
> ***Your Answer***
>
> Raising a domain error and blocking database persistence on illegal transitions guarantees data integrity and prevents physical actuators from entering invalid or unsafe operational modes. An HTTP 400 Bad Request or 409 Conflict is appropriate for this case. These rules must live in the domain layer rather than in React so that business invariants remain protected regardless of whether the request comes from the web UI, an automated controller, or a backend script.

7. Device JSON gains `state` and `allowed_commands`. How does the dashboard use those fields (badges, disable illegal buttons)? How does this prepare **Phase 10 Command**?

> [!NOTE]
> ***Your Answer***
>
>The dashboard uses state to render visual status badges on actuator cards and allowed_commands to know which actions are legal, allowing the UI to display appropriate controls or disable illegal ones. This directly prepares for Phase 10 (Command) by ensuring the command dispatch layer has a reliable, server-validated contract for what operations can be invoked on each device.

## C. Compare, contrast, and scenarios

8. Contrast State with **Strategy**. Both look like “context delegates to an object.” Who typically **changes** the active object, and is the variation a **lifecycle** or a **selectable policy**? Give a greenhouse example of each (this phase vs Phase 6).

> [!NOTE]
> ***Your Answer***
>
> While both patterns delegate behavior behind uniform interfaces, Strategy represents a user-selected or operator-configured policy (such as choosing a conservative versus aggressive watering schedule) where an external actor explicitly changes the active strategy. In contrast, State manages an internal object lifecycle where the active state transitions automatically or via guarded operations triggered by runtime events and system conditions.

9. Contrast State with a pile of booleans (`is_running`, `is_fault`, `is_maintenance`). Why do illegal combinations of flags appear, and how do explicit state objects (or a transition table) prevent that?

> [!NOTE]
> ***Your Answer***
>
>Modeling lifecycle states with a pile of independent boolean flags allows impossible or contradictory combinations to occur. Explicit state objects or a centralized transition table prevent this by restricting the object to exactly one valid state at a time and strictly defining which state transitions are legal.

10. A classmate puts HTTP status mapping or SQLAlchemy commits **inside** a concrete state class. Another state mutates a flag directly and skips `transition` / `set_state`. Explain why each is a trap.

> [!NOTE]
> ***Your Answer***
>
>Putting HTTP status mappings or SQLAlchemy database commits inside a state class is a trap because it pollutes pure domain logic with infrastructure and transport concerns, breaking reusability and unit testability. Mutating state flags directly while skipping transition validation is a trap because it bypasses domain guards, destroying state encapsulation and allowing invalid or corrupt lifecycle transitions to bypass business rules.