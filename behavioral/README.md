# Behavioral Design Patterns

Behavioral patterns manage algorithms, assign responsibilities, and define how objects communicate with one another. They shift focus from object structure to how objects interact at runtime.

## Patterns

| Pattern | Summary |
|---|---|
| Chain of Responsibility | Passes a request along a handler chain until one processes it |
| Command | Encapsulates requests as objects, enabling undo/redo and queuing |
| Interpreter | Defines a grammar and an interpreter to evaluate sentences in that grammar |
| Iterator | Provides sequential traversal of a collection without exposing its representation |
| Mediator | Centralises communication between objects to reduce direct coupling |
| Memento | Captures and restores an object's internal state without violating encapsulation |
| Observer | Notifies all registered subscribers automatically when a subject changes state |
| State | Lets an object alter its behaviour by switching between state objects |
| Strategy | Swaps algorithms at runtime behind a common interface |
| Template Method | Defines the skeleton of an algorithm in a base class, deferring steps to subclasses |
| Visitor | Adds new operations to an object structure without modifying the element classes |

## Directory Layout

Each pattern directory contains:

```
<pattern-name>/
    <pattern_name>.py   # Core implementation
    example_1.py        # First usage scenario
    example_2.py        # Second usage scenario
    example_3.py        # Third usage scenario
    tests/
        test_<pattern_name>.py
```

## Run

```bash
# All behavioral pattern tests
python -m pytest behavioral/ -q

# A single pattern
python -m pytest behavioral/observer-pattern/ -v
```
