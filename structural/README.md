# Structural Design Patterns

Structural patterns explain how to assemble objects and classes into larger structures while keeping those structures flexible and efficient. They use composition and interfaces to form new functionality from existing parts.

## Patterns

| Pattern | Summary |
|---|---|
| Adapter | Converts an incompatible interface into one that clients expect |
| Bridge | Decouples an abstraction from its implementation so both can vary independently |
| Composite | Composes objects into tree structures so clients treat leaves and composites uniformly |
| Decorator | Attaches additional responsibilities to an object at runtime via composition |
| Facade | Provides a simplified interface to a complex subsystem |
| Flyweight | Shares common state between many fine-grained objects to reduce memory usage |
| Proxy | Controls access to another object, adding lazy init, caching, or protection |

## Directory Layout

Each pattern directory contains:

```
<pattern-name>/
    <pattern_name>.py   # Core implementation
    example_1.py        # First usage scenario
    example_2.py        # Second usage scenario
    tests/
        test_<pattern_name>.py
```

## Run

```bash
# All structural pattern tests
python -m pytest structural/ -q

# A single pattern
python -m pytest structural/decorator-pattern/ -v
```
