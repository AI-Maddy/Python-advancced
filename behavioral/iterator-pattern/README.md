# Iterator Pattern

Provides a way to access elements of a collection sequentially without exposing its underlying representation. Python natively supports the iterator protocol via `__iter__` / `__next__`.

## C++ Equivalent
`begin()`/`end()` with `operator++`, `operator*`; or range-based `for` loops with custom iterator types.

## Files

| File | Description |
|---|---|
| `iterator_pattern.py` | Core implementation: `Iterator` ABC, `TreeNode`, `InorderIterator` for a binary tree |
| `example_1.py` | In-order, pre-order, and post-order binary tree iterators |
| `example_2.py` | Paginated API result iterator |
| `example_3.py` | Directory file iterator with filtering |
| `tests/test_iterator_pattern.py` | pytest suite |

## Run

```bash
python iterator_pattern.py          # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Iterator` — ABC with `__iter__` and `__next__` (mirrors `collections.abc.Iterator`)
- `TreeNode` — binary tree node with `__iter__` delegating to `InorderIterator`
- `InorderIterator` — concrete iterator using a stack-based traversal
