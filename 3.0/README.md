# RealEstateCore v3.0

**Modules:**
* [Metadata](metadata/) -- Various annotation properties used to document the entire ontology suite.
* [Core](core/) -- Collects the top-level classes and properties that span over or are reused within multiple REC modules. Imports the Metadata module, and is imported by all other specific child modules.
* [Agents](agents/) -- Basic types of agents (people, organizations, groups), structurally aligned with FOAF.
* [Building](building/) -- Different types of building components and rooms.
* [Device](device/) -- Device types (sensors and actuators), device configuration, device actuation, etc.
* [Lease](lease/) -- Contracts, leasable premises, types of premises, etc.

**Composed Ontology:**
* [REC Full](full/) -- Imports all REC modules, providing the fullest possible expressivity.
