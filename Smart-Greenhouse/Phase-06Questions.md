# Phase 6 — Strategy questions

**Pattern / focus:** Strategy.

**Read first:** [Guide 06](../../materials/guides/06-strategy.md) · [Requirements](requirements.md)

## How to answer

- Use your own wording. Do not paste teaching-example types (for example shipping quotes) as if they were your greenhouse classes.
- When a question asks about *this application*, refer to irrigation (or lighting) policies, location context, and the automation API from the lab.
- Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
- Write each answer inside the matching **Your Answer** note. Replace the placeholder; leave the question text unchanged.

## A. Pattern

1. State the intent of Strategy in plain language. How does the **context** use a strategy, and why must “choose which algorithm” stay separate from “run the algorithm”?

> [!NOTE]
> ***Your Answer***
>
> The intent of the Strategy pattern is to define a family of interchangable algorithms, encapsulate each one behind a common interface, and let them be swapped dynamically at runtime. The context holds a reference to the strategy adn delegates the calculation to it when an evaluation is triggered. Separating ensures that the caller doesn't need to know how the decision is calculated, which keeps the algorithms modular, testable, and decoupled from the client routers.

2. Name the participants (**strategy**, **concrete strategies**, **context**, **client**). What goes wrong when all policies live as `if/elif` inside the context (or inside an HTTP router)?

> [!NOTE]
> ***Your Answer***
>
> Strategy: The abstract interface declaring the evaluation method (decide(context))
>Concrete Strategies: The specific algorithm implementations (ConservativeMoistureStrategy etc..)
>Context: The plain data object carrying the parameters needed to make the decision (LocationAutomationContext)
>Client: The service or API route that resolves the strategy and invokes it.
>When all policies live as if/elif statements inside the context, it violates the Open/Closed Principle. Whenever we have to add or modify a rule, we have to open up and edit existing blocks, which makes the code hard to test and prone to regressions.

3. When should you use Strategy, and when should you skip it (one algorithm only; or the variation is a **lifecycle mode** rather than a chosen policy)?

> [!NOTE]
> ***Your Answer***
>
> When we have multiple ways to calculate a result or make a decision and want to switch between tehm based on user configuration, we should use Strategy. If there is only one algorithm or when the variation represents a state machines's lifecycle mode then we should skip it.

## B. This phase of the application

4. In this lab, what does a strategy’s `decide(context)` return (action + reason)? Give a concrete difference you implemented (or were required to implement) between **conservative** and **aggressive** on the **same** moisture reading and zone thresholds.

> [!NOTE]
> ***Your Answer***
>
>Strategy's decide(context) returns a Recommendation containing an action, a human-readable reason, and an optional score. For the same moisture reading sitting slightly below the zone's low threshold, the aggressive strategy returns an "irrigate" action because it triggers when thresholds are breached, and the conservative strategy migh return a "wait" action because it requires an extra safety buffer before overwatering risk.

5. Where do the numbers in `LocationAutomationContext` (or your equivalent) come from? Latest moisture may already be in `sensor_readings` from a manual read, the simulation sampler, or MQTT translation — why does this phase not add a scheduler or a broker? Why must strategies receive a plain context object, not SQLAlchemy rows or FastAPI types? Why are thresholds read from **zones**, not hardcoded in the strategy class?

> [!NOTE]
> ***Your Answer***
>
> The numbers in the context come by querying persisted database records, fetching the latest readings from sensor_readings, and matching zone thresholds. This phase does not add a schedular or broker because automation evaluation is triggered on-demand via the API in this step, which keeps the focus on strategy execution. Strategies must receive plain context objects to keep domain logic pure and independent of database or transport frameworks. Thresholds are read from zones because different physical zones require customized limits depending on their crops, rather than having rigid constants hardcoded into algorithm classes.


6. The active `strategy_key` is **persisted** per `location_id` (for example in `automation_rules`). Why must `POST .../automation/evaluate` use the **saved** key rather than a key the client sends only in that request? What happens on the next evaluate after the operator changes strategy but moisture stays the same?

> [!NOTE]
> ***Your Answer***
>
> The evaluation endpoint must use the saved key so that automated controllers, background tasks, or subsequent requests evaluate against the operator's official configuration stored in the database, rather than relying on transient client parameters. When an operator updates the saved strategy key, the next evaluation will apply the new algorithm's logic, causing the recommendation to change even if the moisture stays the same.

7. Strategy **recommends** (irrigate / wait). It should not itself start a pump. Why keep **decide** separate from **execute**? Which later pattern is meant to carry out the action?

> [!NOTE]
> ***Your Answer***
>
> Keeping decide separate from execute to the Single Responsibility Principle, the strategy's job is pure decision-making and business policy evaluation, not hardware control. Executing physical actions requires interacting with actuator adapters, handling errors, and logging hardware states. Command or Decorator patterns are meant to carry out this actions.

## C. Compare, contrast, and scenarios

8. Contrast Strategy with **State** (Phase 8). Both delegate to an object with the same shape. Who typically **changes** the active object, and is the variation a **policy** or a **lifecycle**?

> [!NOTE]
> ***Your Answer***
>
> Both patterns delegate behavior to helper objects with similar signatures. Strategy represents a user-chosen policy, where the external client or operator explicitly changes the active strategy, but State represents an internal object lifecycle where the object transitions between different states automatically based on internal conditions and events.

9. Contrast Strategy with **Adapter** (Phase 5) and with **Builder** (Phase 4). Which one translates a foreign API, which one assembles a valid aggregate, and which one swaps an algorithm?

> [!NOTE]
> ***Your Answer***
>
> Adapter translates a foreign API into a normalized shape.
>Builder assembles a complex, valid aggregate step-by-step with validation at the end.
>Strategy swaps out an algorithm or decision-making policy behind a common interface.


10. A classmate writes one “mega-strategy” that still contains `if conservative` / `if aggressive` inside a single class. Another strategy class calls the actuator adapter to water immediately. Explain why each is a trap.

> [!NOTE]
> ***Your Answer***
>
> The mega-strategy with if/elif blocks defeats the purpose of polymorphism, which starts tight coupling and fails the Open/Closed Principle.
> The strategy that calls the actuator adapter directly violates domain purity and separation of concerns by mixing decision logic with hardware execution side-effects, it makes the unit testing difficult and risky.