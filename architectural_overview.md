## architectural overview

the project follows a __layered architecture__ design with dependencies pointing inwards. the core logic is 
isolated in `domain`, orchestrated by `application`, and supported by `infrastructure`.

### fundamental patterns
- __gateway__\
`src/infrastructure/graph_gateway.py`\
encapsulates access to external systems (NetworkX, file system, etc.). it converts raw data sources like files 
or memory objects into __domain__ `Graph` objects.
- __registry__\
`src/domain/*/registry.py`\
`SparsifierRegistry`, `TransformRegistry`, and `MetricRegistry` provide global access points to find plugin classes
by string keys.
- __plugin__\
`src/domain/common/plugin_discovery.py`\
the `discover_modules` function dynamically scans directories and loads modules at runtime. this allows new algorithms
to be added without modifying the core code.
- __separated interface__\
`src/domain/sparsifiers/base.py`\
the abstract base class `Sparsifier(ABC)` defined in the domain separates the definition of what a sparsifier *is* from
its concrete implementations.
- __layer supertype__\
`src/domain/transforms/base.py`\
`GraphTransform` serves as a supertype for all algorithms. it implements the __template method__ in `execute()` 
to handle common logic such as timing, logging, validation, etc. while delegating specific work to `run()`.
- __value object__\
`src/domain/graph_model.py`\
`RunID`, `GraphID`, `RunParams`, and `MetricResult` are immutable objects defined by their attributes (values) rather
than their identity.
- __service stub__\
`src/infrastructure/persistence/stubs.py`\
`InMemoryGraphRepository` simulates a database using a dictionary, which allows the system to run tests and demos
without a real database connection.

### domain logic patterns
- __domain model__\
`src/domain/graph_model.py`\
the `Graph` class contains both data (`_nx`) and behavior (`is_directed`, `to_networkx`) and acts as the core of the 
business logic
- __service layer__\
`src/application/experiment_service.py`\
`ExperimentService` defines the application's boundary; its role is to orchestrate the flow
*fetch data → run algorithm → compute metrics → save results*.
- __strategy__\
`src/domain/sparsifiers/*.py`\
algorithms like `RandomSparsifier` and `IdentitySparsifier` are interchangeable strategies that the service can swap 
at runtime as they all adhere to the `run(graph, params)` interface. 

### object-relational behaviors
- __unit of work__\
`src/infrastructure/persistence/unit_of_work.py`\
maintains a list of objects affected by a "business transaction"; ensures that the result `Graph` object and the `Experiment`
audit trail are committed to storage together atomically or rolled back on error.
- __lazy load__\
`src/domain/graph_model.py`\
implemented via a __virtual proxy__. the `Graph` object is initialized with a `_loader` function, and the heavy 
NetworkX graph `_nx` is only loaded from disk only when `to_networkx()` is called to save memory.
- __repository__\
`src/infrastructure/persistence/repo.py`\
provides a collection-like interface with methods like `save()` and `get()` for accessing Domain objects, mediating between
the __domain__ and the __data mapping__ layers.
4. __distribution patterns__
- __data transfer object__\
`src/application/dto.py`\
`ExperimentDTO` is a simple data container used to carry data from the __service layer__ to the "outer world" of CLI and tests.
it decouples the presentation layer from the internal domain model.