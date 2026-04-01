# Creational Design Patterns

Creational patterns deal with object creation mechanisms, aiming to create objects in a manner that is suitable to the situation. They decouple the client from the concrete classes being instantiated.

## Patterns

| Pattern | Summary |
|---|---|
| Abstract Factory | Creates families of related objects without specifying their concrete classes |
| Builder | Separates step-by-step construction of a complex object from its representation |
| Factory Method | Defines an interface for creating an object, but lets subclasses decide the type |
| Prototype | Creates new objects by cloning an existing instance |
| Singleton | Ensures a class has only one instance and provides a global access point to it |

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
# All creational pattern tests
python -m pytest creational/ -q

# A single pattern
python -m pytest creational/factory-method-pattern/ -v
```
