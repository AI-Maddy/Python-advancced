# Abstract Factory Pattern

Provides an interface for creating families of related or dependent objects without specifying their concrete classes. Ensures that products from the same factory are compatible with each other.

## C++ Equivalent
Abstract factory class with pure virtual `createButton()`, `createCheckbox()`, etc.; concrete factories produce consistent platform-specific widget sets.

## Files

| File | Description |
|---|---|
| `abstract_factory.py` | Core implementation: `Button`, `Checkbox`, `Dialog` ABCs; `WindowsFactory`, `MacOSFactory`, `LinuxFactory` |
| `example_1.py` | Cross-platform UI widget creation |
| `example_2.py` | Database driver family (connection, cursor, transaction) |
| `tests/test_abstract_factory.py` | pytest suite |

## Run

```bash
python abstract_factory.py          # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Button`, `Checkbox`, `Dialog` — abstract product ABCs
- `WindowsButton`, `MacOSButton`, etc. — concrete products per platform
- `UIFactory` — abstract factory ABC
- `WindowsFactory`, `MacOSFactory`, `LinuxFactory` — concrete factories
