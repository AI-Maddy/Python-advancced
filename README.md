# Python Advanced — OOP, Patterns & Idioms

A complete Python advanced track ported from a C++ OOP & design patterns curriculum.
Covers 30-day Python OOP course, all 23 GoF design patterns, and Pythonic idioms.

## Structure

| Directory | Contents |
|---|---|
| `30-days/` | 30-day Python OOP course (lesson, exercises, solutions, tests per day) |
| `behavioral/` | 11 behavioral design patterns with examples and tests |
| `creational/` | 5 creational design patterns with examples and tests |
| `structural/` | 7 structural design patterns with examples and tests |
| `python-idioms/` | 12 Pythonic idioms (RAII, descriptors, protocols, metaclasses, etc.) |
| `MKwebsite/` | MkDocs documentation site |

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest . -q          # run all 1100+ tests
```

## Documentation

Start the MkDocs site:
```bash
cd MKwebsite && mkdocs serve --dev-addr 127.0.0.1:3019
```

## Python vs C++ Map

| C++ | Python |
|---|---|
| RAII | Context manager (`with`) |
| `virtual` | All methods are virtual |
| Template `<T>` | `TypeVar` + `Generic[T]` |
| Pure virtual / interface | `ABC` + `@abstractmethod` / `Protocol` |
| Rule of Zero | `@dataclass` |
| Tag dispatch | `functools.singledispatch` |
| Type erasure | `Protocol` / `ABC` |
| Catch2 | `pytest` |
