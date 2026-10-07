# Phase 5 — Adapter questions

**Pattern / focus:** Adapter.

**Read first:** [Guide 05](../../materials/guides/05-adapter.md) · [Requirements](requirements.md)

## How to answer

- Use your own wording. Do not paste teaching-example types (for example a legacy XML calendar client) as if they were your greenhouse classes.
- When a question asks about *this application*, refer to sensor ports, adapters, readings, and `sensor_readings` from the lab.
- Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
- Write each answer inside the matching **Your Answer** note. Replace the placeholder; leave the question text unchanged.

## A. Pattern

1. State the intent of Adapter in plain language. What problem appears when business code speaks a vendor or legacy protocol (odd field names, units, XML, status codes) directly?

> [!NOTE]
> ***Your Answer***
>
> The intent of the Adapter pattern is to allow incompatible interfaces to work with a matching adapter interface that translates one format into another. When business code speaks a vendor or legacy protocol directly,then it causes widespread code changes and tight coupling whenever a vendor changes their API or hardware specs.

2. Name the participants (**target / port**, **adaptee**, **adapter**, **client**). What does the adapter translate, and what must it **not** decide (business policy)?

> [!NOTE]
> ***Your Answer***
>
> Target/port:- The domain interface expected by the client. Adaptee:- The existing incompatible service, SDK, or raw payload format. Adapter:- Teh concrete translator. Client:- The application service or components which depends on the target port. The adapter translates raw payloads, shapes, or units into the unified domain structure, but it must not decide busines policies which belong in the domain/application layer.

3. GoF distinguishes an **object adapter** (composition) from a **class adapter** (inheritance). Which does modern code prefer, and why?

> [!NOTE]
> ***Your Answer***
>
> Modern code prefers the object adapter pattern using composition because object composition is more flexible which allows wrapping multiple or changing adaptee implementations dynamically at runtime.

## B. This phase of the application

4. What is `SensorPort` in this lab, and what normalized value type (for example `Reading`) do adapters return? Why do application services depend on the port rather than on a simulation driver or vendor SDK?

> [!NOTE]
> ***Your Answer***
>
> The SensorPort is an domain port interface in this lab. Adapters return a normalized value object containing value, unit, source, and timestamp fields. Application services depend on the port rather than on a simulation driver or vendor SDK to maintain clean architecture. This also ensures that any changes to vendor libraries or simulation logic do not completely affect the business workflows.

5. You need three translations onto the same normalized reading: a simulation adapter, a vendor stub, and an MQTT translator that accepts a payload dict. Why is the different raw shape the point of the exercise? How does `source` (`simulation`, `vendor`, or `mqtt`) show which adapter produced the reading, and why must the MQTT translator not open a broker in this phase? Phase 12 may deliver that same dict on a device HTTP route or through an optional broker — why must this phase still not open either transport?

> [!NOTE]
> ***Your Answer***
>
> The differnt raw shape is the point of the excercise to normalize the differnt input formats into a uniform shape. The source field records which adapter produced the reading. Because this phase focuses on translation and persistence mechanics without running live networking transports, the mqtt translator does not open a broker in this phase.

6. Readings are **appended** to `sensor_readings` (history grows). Why not keep only the latest value in memory or overwrite a single row, and which later phase consumes this history? Why do a manual read, the simulation sampler, and (later) MQTT share **one** writer of that table? Why does the sampler skip devices with tracking off and MQTT devices, and why do sensor cards poll the latest stored reading until Phase 12?

> [!NOTE]
> ***Your Answer***
>
> Readings are appended for the future auditings, charts, and later strategy evaluations. We use the one writer of the table to maintain database consistency and single point-of-truth. The sampler skips the devices with tracking off and mqtt devices because they should not be automatically sampled by the background loop.

7. `POST /api/sensors/{id}/read` runs an adapter, persists, and returns a DTO. What HTTP status is appropriate when the device is missing versus when the adapter fails? Why must the router never see vendor-shaped types?

> [!NOTE]
> ***Your Answer***
>
> When a device is missing HTTP 404 Not Found status is appropriate, and when the adapter fails HTTP 400 Bad Request status is appropriate. Because router should only communicate via normalized DTOs to keep transport contracts independent of any specific provider's technology.

## C. Compare, contrast, and scenarios

8. Contrast Adapter with **Facade**. Adapter changes the **shape** of an existing interface; Facade simplifies **how to use** a subsystem. Give a greenhouse-shaped example of each (Adapter this phase; Facade in Phase 7).

> [!NOTE]
> ***Your Answer***
>
>An Adapter changes the interface of an existing class or component to match what a client expects, and a Facade simplifies interaction with a complex subsystem by providing a unified, higher-level interace. Adapter translates a vendor's raw payload dictionary inro a normalized Reading object in this phase. Facades provides a single entry point to orchestrate environmental control systems across actuators and automations later.

9. Contrast Adapter with **Decorator**. Both wrap an object. What is different about the interface they present to the client?

> [!NOTE]
> ***Your Answer***
>
> An Adapter changes the interface of the wrapped object to match a different target interface required by the client. A Decorator preserves the exact same interface as the wrapped object, and modifies its behavior transparently without altering its signature. 

10. A classmate puts irrigation policy (“if moisture &lt; 0.3 then water”) inside the vendor adapter. Why is that a trap? Where should that decision live instead (later Strategy), and what should stay in the adapter?

> [!NOTE]
> ***Your Answer***
>
>Because adpaters are strictly responsible for data translation and protocol normalization, putting irrigation policy inside an adapter is a trap. The policy should live in an automation rule or evaluation engine, and the adapter should be translating raw sensor inputs into normalized domain values only.