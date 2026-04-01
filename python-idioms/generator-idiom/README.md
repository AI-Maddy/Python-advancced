# Generator Idiom

Generator functions use `yield` to produce values lazily, enabling infinite sequences and memory-efficient pipelines. The full coroutine protocol (`send`, `throw`, `close`) and `yield from` delegation are also covered.

## C++ Equivalent
Lazy range adaptors (`std::ranges`), coroutines (`co_yield` in C++20), or explicit iterator classes.

## Files

| File | Description |
|---|---|
| `generator_idiom.py` | Core implementation: `fibonacci()`, `countdown()`, `send()`/`throw()` protocol, `yield from`, pipeline composition |
| `example_1.py` | Data processing pipeline using generator chaining |
| `example_2.py` | Infinite sequence generators with `itertools` integration |
| `tests/test_generator_idiom.py` | pytest suite |

## Run

```bash
python generator_idiom.py           # demo
python -m pytest tests/ -v          # tests
```

## Key Concepts

- `yield` — suspends the function and emits a value
- Generator expression — `(x for x in iterable if condition)`
- `send(value)` — resume and inject a value into the generator
- `yield from` — delegate to a sub-generator, forwarding `send`/`throw`
- Pipeline composition — chain generators for lazy data transformation
