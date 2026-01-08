## architectural overview

the project follows a __layered architecture__ design style with dependencies pointing inwards. the core logic is 
isolated in `domain`, orchestrated by `application`, and supported by `infrastructure`.

1. __fundamental patterns__
- __gateway__
`src/infrastructure/graph_gateway.py`
encapsulates access to external systems (NetworkX, file system, etc.). it converts raw data sources like files 
or memory objects into Domain `Graph` objects.
- __registry__
`src/domain/*/registry.py`
`SparsifierRegistry`, `TransformRegistry`, and `MetricRegistry` provide global access points to fund plugin classes
by string keys.
- __plugin__
`src/domain/common/plugin_discovery.py`
the `discover_modules` function dynamically scans directories and loads modules at runtime. this allows new algorithms
to be added without modifying the core code.
- __separated interface__
`src/domain/sparsifiers/base.py`
- __layer supertype__
- __value object__
- __service stub__
2. __domain logic patterns__
3. __object-relational behaviors__
4. __distribution patterns__