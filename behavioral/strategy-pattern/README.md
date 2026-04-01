# Strategy Pattern

Defines a family of algorithms, encapsulates each one, and makes them interchangeable. The strategy lets the algorithm vary independently from the clients that use it.

## C++ Equivalent
Abstract base class with virtual `execute()`, or `std::function` + lambdas for lightweight strategies.

## Files

| File | Description |
|---|---|
| `strategy_pattern.py` | Core implementation: `SortStrategy` ABC, `BubbleSortStrategy`, `QuickSortStrategy`, and a `Sorter` context |
| `example_1.py` | Sorting strategy swap at runtime |
| `example_2.py` | Payment processing strategies (credit card, PayPal, crypto) |
| `example_3.py` | Compression strategies (zip, gzip, lzma) |
| `tests/test_strategy_pattern.py` | pytest suite |

## Run

```bash
python strategy_pattern.py          # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `SortStrategy` — ABC with `sort(data)` method
- `BubbleSortStrategy`, `QuickSortStrategy`, `MergeSortStrategy` — concrete strategies
- `Sorter` — context that holds and delegates to a strategy
