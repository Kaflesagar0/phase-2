# Phase 9 — Decorator questions

**Pattern / focus:** Decorator.

**Read first:** [Guide 09](../../materials/guides/09-decorator.md) · [Requirements](requirements.md)

## How to answer

- Use your own wording. Do not paste teaching-example types (for example HTTP client wrappers) as if they were your greenhouse classes.
- When a question asks about *this application*, refer to `ActuatorPort`, policy decorators, and `actuator_execution_log` from the lab.
- Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
- Write each answer inside the matching **Your Answer** note. Replace the placeholder; leave the question text unchanged.

## A. Pattern

1. State the intent of Decorator in plain language. Why is stacking wrappers a flexible alternative to a combinatorial explosion of subclasses (`LoggingRetryMaxRuntimeActuator`, …)?

> [!NOTE]
> ***Your Answer***
>
> The purpose of the Decorator pattern is to add extra features or behaviors to an existing object without changing its original code. It works by wrapping the object with other classes that add new functions. Stacking wrappers is more flexible because we can combine different features, such as logging and retry, without creating a separate subclass for every possible combination. This also makes the code easier to manage and update.

2. Name the participants (**component**, **concrete component**, **decorator**, **concrete decorators**). What interface does every decorator present to the caller, and why must that match the wrapped component?

> [!NOTE]
> ***Your Answer***
>
> Component: The main interface (ActuatorPort).
>Concrete Component: The actual implementation (SimulationActuatorAdapter).
>Decorator: The base class that wraps another component and follows the same interface.
>Concrete Decorators: The classes that add extra features, such as LoggingActuatorDecorator and MaxRunTimeActuatorDecorator.
>Every decorator uses the same interface (ActuatorPort) as the original component. This is important because it allows us to wrap multiple decorators together without changing how the application uses them. The caller does not need to know how many wrappers are being used.

3. **Order matters.** Using logging and retry (or logging and max-run-time) as an example, explain how wrapping A around B can change what you observe compared with wrapping B around A.

> [!NOTE]
> ***Your Answer***
>
> The order of decorators matters because it affects how the methods are executed. For example, if LoggingActuatorDecorator is placed outside MaxRunTimeActuatorDecorator, the logging decorator can record the execution attempt, even if the max-run-time policy blocks it.
>However, if MaxRunTimeActuatorDecorator is placed outside the logging decorator, it might block the execution before the logging decorator gets called. This means the blocked attempt might not be recorded. So, changing the order can affect what gets logged and which policies are applied.

## B. This phase of the application

4. What is `ActuatorPort` here, and which **at least two** decorators did you stack around the real adapter (for example logging and max run-time)? Where is the chain wired (composition root / factory), and why not inside the HTTP router?

> [!NOTE]
> ***Your Answer***
>
> ActuatorPort is the interface used to send commands to an actuator. We used two decorators: LoggingActuatorDecorator and MaxRunTimeActuatorDecorator, which wrap the SimulationActuatorAdapter.
>The chain is connected in the composition root or factory to keep the HTTP router simple and focused only on handling requests.

5. Max run-time can **short-circuit**: the inner adapter is never called. Why must a blocked attempt still produce a row in `actuator_execution_log` with `success=false` and the policy named in `policy_applied`?

> [!NOTE]
> ***Your Answer***
>
> Blocked attempts should still be saved in the database so the system has a complete record of all executions. Saving success=false and the policy name also helps us understand why the command was blocked.

6. How does max run-time know the actuator has been running too long (for example `actuator_states.updated_at` from Phase 8)? Why is that data from **State**, not something the decorator should invent as a second lifecycle?

> [!NOTE]
> ***Your Answer***
>
> The decorator checks the actuator_states table and uses the updated_at timestamp to see how long the actuator has been running. This information comes from Phase 8, so there is no need to create another system to track the actuator's state.

7. `GET /api/actuators/executions` feeds the dashboard execution log. Why persist attempts in the database instead of only printing to stdout? What should the UI show after a blocked attempt and a refresh?

> [!NOTE]
> ***Your Answer***
>
> Saving attempts in the database allows the dashboard to display them even after refreshing the page. Unlike console messages, database records can be accessed later. After a blocked attempt, the UI should show success=false, the applied policies, and the error message "Max run time exceeded".

## C. Compare, contrast, and scenarios

8. Contrast Decorator with **Adapter**. Both wrap. One **keeps** the interface and **adds** behaviour; the other **changes** the interface and **translates**. Which is which in this greenhouse (Phase 9 vs Phase 5)?

> [!NOTE]
> ***Your Answer***
>
> The Adapter pattern (Phase 5) changes an interface so different parts of the application can work together. The Decorator pattern (Phase 9) keeps the same interface but adds extra features, such as logging and max-run-time checking.

9. Contrast Decorator with **inheritance** of combined policies. How does composition let you add or remove a policy without a new subclass for every combination?

> [!NOTE]
> ***Your Answer***
>
> Inheritance requires creating a new subclass for every combination of features, which makes the code complicated. With Decorator, we can simply add, remove, or combine wrappers without creating new subclasses. This makes the code easier to manage.

10. A classmate’s decorator changes the method signature “a little” (extra required argument, different return type). Another ignores wrap order and cannot explain whether logging runs once per logical call or per inner attempt. Explain why each is a trap.

> [!NOTE]
> ***Your Answer***
>
>Changing the method signature is a problem because every decorator must use the same interface as the original component. Otherwise, it can break how the application uses it.Ignoring the decorator order can also cause problems because logging might happen at the wrong time or record attempts more than once. We need to understand the order to make sure everything works correctly.