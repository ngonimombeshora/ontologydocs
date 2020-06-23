# RealEstateCore v3.1.3

**Modules:**
* [Metadata](metadata.html) -- Various annotation properties used to document the entire ontology suite.
* [Core](core.html) -- Collects the top-level classes and properties that span over or are reused within multiple REC modules. Imports the Metadata module, and is imported by all other specific child modules.
* [Actuation](actuation.html) -- The actuation model; message semantics for requesting and enacting actuation on building systems.
* [Agents](agents.html) -- Basic types of agents (people, organizations, groups), structurally aligned with FOAF.
* [Analytics](analytics.html) --  A vocabulary for describing prognoses and aggregates, and the processes used to generate these.
* [Building](building.html) -- Different types of building components and rooms.
* [Data schemas](dataschemas.html) -- Primitive and complex (object/array) data schemas for sensors, actuators, services, etc.
* [Device](device.html) -- Device types (sensors and actuators), device configuration, device actuation, etc.
* [Lantmäteriet](lantmäteriet.html) -- Optional module covering the data model used by the Swedish National Land Survey, in its database Swedish Real Property Register (not included in the Full ontology below).
* [Lease](lease.html) -- Contracts, leasable premises, types of premises, etc.

**Composed Ontology:**
* [REC Full](full.html) -- Imports all REC modules, providing the fullest possible expressivity.
