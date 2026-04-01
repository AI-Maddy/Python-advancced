# Template Method Pattern

Defines the skeleton of an algorithm in a base class, deferring some steps to subclasses. Subclasses can redefine certain steps without changing the algorithm's overall structure.

## C++ Equivalent
Non-virtual public method calls private/protected virtual methods; subclasses override the virtual steps.

## Files

| File | Description |
|---|---|
| `template_method_pattern.py` | Core implementation: `DataProcessor` ABC with `process()` template method (read → transform → write) |
| `example_1.py` | CSV and JSON data processors |
| `example_2.py` | Report generators (HTML, PDF, plain text) |
| `example_3.py` | Build pipeline steps (compile, test, package) |
| `tests/test_template_method_pattern.py` | pytest suite |

## Run

```bash
python template_method_pattern.py   # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `DataProcessor` — ABC; `process()` is the template method orchestrating `read()` → `transform()` → `write()`
- `before_process()` / `after_process()` — optional hook methods with default no-op implementations
- Concrete processors override the abstract steps without touching `process()`
