# Abstract Base Class Idiom

`abc.ABC` and `@abstractmethod` define interfaces that subclasses must implement. `__subclasshook__` enables virtual subclasses that satisfy an interface without explicit inheritance. `collections.abc` provides ready-made ABCs for common protocols.

## C++ Equivalent
Pure virtual class (`= 0` methods); interface classes with no data members.

## Files

| File | Description |
|---|---|
| `abstract_base_class.py` | Core implementation: `Shape` ABC, `@classmethod @abstractmethod`, `@property @abstractmethod`, `__subclasshook__`, `collections.abc` examples |
| `example_1.py` | Shape hierarchy with enforced `area()` and `perimeter()` |
| `example_2.py` | Custom `Sequence` implementation satisfying `collections.abc.Sequence` |
| `tests/test_abstract_base_class.py` | pytest suite |

## Run

```bash
python abstract_base_class.py       # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `ABC` / `ABCMeta` — marks a class as abstract; prevents direct instantiation
- `@abstractmethod` — subclasses must override; raises `TypeError` at class creation if not
- `@classmethod @abstractmethod` — abstract named constructors
- `@property @abstractmethod` — abstract properties
- `__subclasshook__` — makes `isinstance` work without explicit inheritance
- `collections.abc` — `Sequence`, `Mapping`, `Iterable`, `Iterator`, `MutableSequence`
