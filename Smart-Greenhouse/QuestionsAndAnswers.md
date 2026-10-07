How to answer
Use your own wording. Do not paste teaching-example types (for example courier notifiers) as if they were your greenhouse classes.
When a question asks about this application, refer to sensors, creators, the devices table, and the sensors API from the lab.
Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
Write each answer inside the matching Your Answer note. Replace the placeholder; leave the question text unchanged.
A. Pattern
State the intent of Factory Method in plain language. What problem appears when callers scatter new / constructors (or a growing if type == ...) across the application?
Note
Answer:
The intent of the Factory Method is to define an interface for creating an object while subclasses or creator classes could decide teh concrete details. When callers scatter direct constructors or grow if type across the application then it would increase the code duplication, testing complexity and the risk of regression.



Name the main participants of Factory Method (product, concrete product, creator, concrete creator, client). For each, give one sentence: what it is responsible for.
Note

Answer:
Product:- It defines the common interface or base data contract.
Concrete Product:- If implements the product interfaces with specific behaviors, fields, or default values.
Creator:- It Declares the abstract factory method that returns a product instance.
Concrete Creator: It Overrides the factory method to assemble.
Client:- It invokes the creator's creation method to obtain a product.



How do you add a new product variant when creators are polymorphic (new class + registry entry) versus when creation lives in one shared if/elif function? Why does that difference matter for extension?
Note

Answer:
WIth polymorphic creators, we simply write a new creator class and add its key to a lookup dictionary but with a shared if/elif function, we must reopen and edit an existing conditional function every single time. The polymorphic approach is better for extension because adding new features by adding fresh code is much safer.



B. This phase of the application
In this lab, what is the product and what are the concrete creators? Why must the API handler (or sensor service) go through a creator/registry instead of constructing MoistureSensor / LightSensor itself?
Note

Answer:
The product is Python Sensor entity, and the concrete creators are MoistureSensorCreator and LightSensorCreator.  The API route must use the registry and creators so it doesn't have to know anything about default configurations, units, or specific sensor setup logic.



POST /api/sensors accepts a short type key such as "moisture" or "light", while the stored/returned field is device_type (for example moisture_sensor). Why are those two fields different? Who decides the stored device_type and default_config?
Note
Answer:

The moisture and light are just a easier name for the frontend and the device_type is the name permanently stored in the database. The concrete creator decides the official device_type and default_config when it builds the sensor.


Why is there a single devices table with role="sensor" instead of a dedicated sensors table? What later phase does that choice prepare for?
Note

Answer:
Using a single devices table with role sensor keeps all the greenhouse hardware in a shared table instead of creating separate tables for every device category. This prepares for the next phase, Phase 3.


What should happen when the client posts an unknown type? Where should that rejection be decided (registry/service vs router constructing a concrete class anyway)?
Note

Answer:
There should be 400 bad request error and an error message showing the supported tyoes. The rejection should happen in teh registry/service layer when looking up the type key.



C. Compare, contrast, and scenarios
Contrast Factory Method with a simple factory (one function full of if type == ...). When is the simple factory “good enough,” and why does this phase still want polymorphic creators?
Note

Answer:
A simple factory uses one function with an if/elif ladder, while factory method uses separate creator classes for each type. A simple factory is good enough for small, simple apps which are not going to change. We use polymorphic creators to make it easy to grow the system in future phases.


Contrast Factory Method with Abstract Factory (Phase 3). Factory Method answers which question? Abstract Factory answers which different question? Why is Factory Method enough for Phase 2 sensors?
Note

Answer:
Factory method answers "how do I create one specific item without tying to its exact class?". Abstract factory answers "how do I create a whole matching set of related itemd together?". Because we are only creating individual sensors on their own, factory method is enough for phase 2 sensors.


A classmate puts SQLAlchemy session commits (or FastAPI request parsing) inside a concrete creator. Why is that a trap? Where should persistence and HTTP stay instead?
Note

Answer:
Putting SQLAlchemy commits inside a creator is a trap because it tangles pure business rules with web and database tools. HTTP must stay in the API layer and database commits must stay in the repository layer.


