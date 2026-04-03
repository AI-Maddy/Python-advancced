# :material-arrow-right-bold-circle: Day 12 — Iterators & Generators

!!! abstract "Day at a Glance"
    **Goal:** Master the iterator protocol, generator functions, `yield from`, lazy pipelines, `itertools`, and coroutine-style generators with `send()`.
    **C++ Equivalent:** Day 12 of Learn-Modern-CPP-OOP-30-Days (`begin()`/`end()`, range-for, `std::generator` C++23)
    **Estimated Time:** 60–90 minutes

<div class="grid cards" markdown>
- :material-lightbulb-on: **Core Concept** — generators are suspended functions; each `yield` is a checkpoint that hands control back to the caller
- :material-snake: **Python Way** — write `yield` and Python creates the entire iterator machinery for you; no class boilerplate required
- :material-alert: **Watch Out** — generators are single-use; once exhausted they silently return nothing — always re-create them
- :material-check-circle: **By End of Day** — build custom iterators, infinite sequences, lazy file pipelines, and coroutine-style data processors
</div>

## :material-lightbulb-on: Intuition

!!! info "Core Idea"
    The *iterator protocol* is just two methods: `__iter__` returns an iterator, and `__next__` returns the next value or raises `StopIteration`.
    A *generator function* — any function containing `yield` — implements this protocol automatically.
    Python suspends the function's frame (local variables, instruction pointer) at each `yield` and resumes it exactly where it stopped.
    This makes generators perfect for infinite sequences and lazy pipelines that process data without loading it all into memory.

!!! success "Python vs C++"
    | Python | C++ |
    |--------|-----|
    | `__iter__` / `__next__` | `begin()` / `end()`, `operator++`, `operator*` |
    | `yield` generator | `co_yield` (`std::generator`, C++23) |
    | `yield from sub` | Delegation to sub-range |
    | Generator expression | Ranges / views (C++20) |
    | `itertools.chain` | `std::ranges::views::join` |
    | `itertools.islice` | `std::ranges::views::take` |
    | `send(value)` coroutine | `co_await` producer pattern |
    | Lazy pipeline | `std::ranges` view composition |

## :material-chart-flow: Generator Lifecycle

```mermaid
flowchart TD
    A([Created\ngen = my_gen()]) --> B([Running\nnext&#40;gen&#41; called])
    B --> C{yield reached?}
    C -- Yes --> D([Suspended\nvalue yielded to caller])
    D --> E{next&#40;&#41; or send&#40;&#41; called again?}
    E -- Yes --> B
    E -- "close() / GC" --> F([Closed\nGeneratorExit raised inside])
    C -- "return / fall off end" --> G([Exhausted\nStopIteration raised])
    F --> G

    style A fill:#4a90d9,color:#fff
    style D fill:#f0a500,color:#fff
    style G fill:#e05252,color:#fff
    style F fill:#888,color:#fff
```

## :material-book-open-variant: Lesson

### The Iterator Protocol

```python
class CountUp:
    """Counts from `start` to `stop - 1`, one step at a time."""

    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self   # the object is its own iterator

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


for n in CountUp(1, 5):
    print(n, end=" ")   # 1 2 3 4

# iter() / next() manually
it = iter(CountUp(10, 13))
print(next(it))   # 10
print(next(it))   # 11
```

### Generator Functions — `yield`

```python
def count_up(start: int, stop: int):
    """Same as CountUp above, but in 3 lines."""
    for n in range(start, stop):
        yield n


for n in count_up(1, 5):
    print(n, end=" ")   # 1 2 3 4
```

### Generator Expressions — Lazy Comprehensions

```python
# List comprehension — eager, builds entire list in memory
squares_list = [x**2 for x in range(1_000_000)]

# Generator expression — lazy, computes one element at a time
squares_gen = (x**2 for x in range(1_000_000))

import sys
print(sys.getsizeof(squares_list))  # ~8 MB
print(sys.getsizeof(squares_gen))   # 200 bytes

total = sum(squares_gen)            # consumed lazily
```

### Infinite Sequences

```python
def fibonacci():
    """Infinite Fibonacci sequence — never raises StopIteration."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


from itertools import islice

# Take the first 10 terms
print(list(islice(fibonacci(), 10)))
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### `yield from` — Delegation

```python
def flatten(nested):
    """Recursively flatten a nested list structure."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # delegate to sub-generator
        else:
            yield item


data = [1, [2, 3, [4, 5]], 6, [7, [8, [9]]]]
print(list(flatten(data)))   # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Binary Tree In-Order Iterator

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Iterator


@dataclass
class TreeNode:
    value: int
    left: Optional[TreeNode] = None
    right: Optional[TreeNode] = None


def inorder(node: Optional[TreeNode]) -> Iterator[int]:
    if node is None:
        return
    yield from inorder(node.left)
    yield node.value
    yield from inorder(node.right)


#        4
#       / \
#      2   6
#     / \ / \
#    1  3 5  7
root = TreeNode(4,
    left=TreeNode(2, TreeNode(1), TreeNode(3)),
    right=TreeNode(6, TreeNode(5), TreeNode(7))
)

print(list(inorder(root)))   # [1, 2, 3, 4, 5, 6, 7]
```

### `itertools` Essentials

```python
import itertools

# chain — concatenate iterables
print(list(itertools.chain([1, 2], [3, 4], [5])))
# [1, 2, 3, 4, 5]

# islice — take N from any iterable
print(list(itertools.islice(fibonacci(), 5, 10)))
# [5, 8, 13, 21, 34]  (skip first 5, take next 5)

# count — infinite arithmetic sequence
counter = itertools.count(start=0, step=2)
print(list(itertools.islice(counter, 6)))   # [0, 2, 4, 6, 8, 10]

# cycle — repeat an iterable forever
colours = itertools.cycle(["red", "green", "blue"])
print([next(colours) for _ in range(7)])
# ['red', 'green', 'blue', 'red', 'green', 'blue', 'red']

# groupby — group consecutive identical keys
data = [("a", 1), ("a", 2), ("b", 3), ("b", 4), ("a", 5)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# a [('a', 1), ('a', 2)]
# b [('b', 3), ('b', 4)]
# a [('a', 5)]

# product — cartesian product
print(list(itertools.product([1, 2], ["a", "b"])))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
```

### Lazy CSV Pipeline

```python
import csv
from pathlib import Path
from typing import Iterator


def read_rows(path: str) -> Iterator[dict]:
    """Yield rows one at a time — never loads the whole file."""
    with open(path, newline="") as f:
        yield from csv.DictReader(f)


def filter_rows(rows: Iterator[dict], key: str, value: str) -> Iterator[dict]:
    for row in rows:
        if row.get(key) == value:
            yield row


def extract_field(rows: Iterator[dict], field: str) -> Iterator[str]:
    for row in rows:
        yield row[field]


# Pipeline — each stage is lazy; nothing runs until the for-loop consumes
# (Assume sales.csv has columns: region, product, revenue)
pipeline = extract_field(
    filter_rows(read_rows("sales.csv"), "region", "North"),
    "revenue"
)
# total = sum(float(x) for x in pipeline)
```

### `send()` — Coroutine-style Generators

```python
def running_average() -> "Generator[float, float, None]":
    """
    Coroutine that accumulates values sent to it and yields the running mean.
    Start with next(gen) or gen.send(None) to prime it.
    """
    total = 0.0
    count = 0
    average = 0.0
    while True:
        value = yield average      # yield current avg, receive next value
        if value is None:
            break
        total += value
        count += 1
        average = total / count


gen = running_average()
next(gen)              # prime the generator (advance to first yield)
print(gen.send(10))    # 10.0
print(gen.send(20))    # 15.0
print(gen.send(30))    # 20.0
print(gen.send(40))    # 25.0
gen.close()            # inject GeneratorExit
```

## :material-alert: Common Pitfalls

!!! warning "Generators are single-use"
    ```python
    gen = (x**2 for x in range(5))
    print(list(gen))    # [0, 1, 4, 9, 16]
    print(list(gen))    # []  — already exhausted!

    # Fix: use a function that returns a new generator each time
    def squares(n):
        return (x**2 for x in range(n))
    ```

!!! danger "Forgetting to prime a coroutine"
    ```python
    gen = running_average()
    gen.send(10)   # TypeError: can't send non-None value to a just-started generator

    # Must advance to first yield first:
    next(gen)      # or gen.send(None)
    gen.send(10)   # now works
    ```

!!! warning "`groupby` only groups *consecutive* equal elements"
    ```python
    import itertools
    data = [1, 1, 2, 1, 1]  # data is NOT fully sorted
    groups = {k: list(v) for k, v in itertools.groupby(data)}
    print(groups)   # {1: [1, 1], 2: [2]}  — last '1 1' group is LOST!

    # Fix: sort first if you want all equal items together
    groups = {k: list(v) for k, v in itertools.groupby(sorted(data))}
    ```

## :material-help-circle: Flashcards

???+ question "Q1 — What is the iterator protocol?"
    An object is an *iterable* if it implements `__iter__()` returning an iterator.
    An *iterator* implements both `__iter__()` (returns `self`) and `__next__()` (returns next value or raises `StopIteration`).
    Iterators are always their own iterables.

???+ question "Q2 — What does `yield from sub` do?"
    It delegates iteration to the sub-iterable `sub`, forwarding each yielded value up to the caller.
    It also forwards `send()` values and exceptions into `sub` (important for coroutines).
    It replaces `for item in sub: yield item` with a single line that is also more efficient.

???+ question "Q3 — How do generator expressions differ from list comprehensions?"
    A list comprehension `[expr for x in it]` is *eager* — it builds the entire list in memory immediately.
    A generator expression `(expr for x in it)` is *lazy* — it computes one value at a time when iterated, using O(1) memory regardless of the input size.

???+ question "Q4 — What is the purpose of `next(gen)` before the first `send()`?"
    A generator starts in the *created* state and must be advanced to the first `yield` before it can accept a non-`None` send value.
    `next(gen)` is equivalent to `gen.send(None)` and advances the generator to its first suspension point.

## :material-clipboard-check: Self Test

=== "Question 1"
    Write a generator `chunked(iterable, size)` that yields successive non-overlapping chunks of length `size` from any iterable.
    Example: `list(chunked(range(9), 3))` → `[[0,1,2], [3,4,5], [6,7,8]]`.

=== "Answer 1"
    ```python
    from itertools import islice
    from typing import Iterator, TypeVar

    T = TypeVar("T")


    def chunked(iterable, size: int) -> Iterator[list]:
        it = iter(iterable)
        while True:
            chunk = list(islice(it, size))
            if not chunk:
                return
            yield chunk


    print(list(chunked(range(9), 3)))   # [[0,1,2],[3,4,5],[6,7,8]]
    print(list(chunked("abcde", 2)))    # [['a','b'],['c','d'],['e']]
    ```

=== "Question 2"
    What is printed? Why?
    ```python
    def gen():
        print("A")
        yield 1
        print("B")
        yield 2
        print("C")

    g = gen()
    print("before next")
    v = next(g)
    print(f"got {v}")
    v = next(g)
    print(f"got {v}")
    ```

=== "Answer 2"
    ```
    before next
    A
    got 1
    B
    got 2
    ```
    Generator bodies do not execute until `next()` is called.
    Each `next()` resumes the frame from the previous `yield` and runs until the next `yield` (printing the letters along the way).
    `"C"` is never printed because we never call `next(g)` a third time.

## :material-check-circle: Summary

!!! success "Key Takeaways"
    - The iterator protocol requires `__iter__` and `__next__`; raising `StopIteration` signals exhaustion
    - Generator functions (`yield`) implement the protocol automatically with frame suspension
    - Generator expressions are lazy counterparts of list comprehensions — O(1) memory
    - Infinite generators paired with `itertools.islice` are safe and memory-efficient
    - `yield from sub` delegates iteration and is more than syntactic sugar — it tunnels `send()` and `throw()`
    - `itertools` (chain, islice, count, cycle, groupby, product) builds powerful lazy pipelines without custom code
    - `groupby` only groups *consecutive* equal keys — sort the data first for a global grouping
    - Coroutine generators receive values via `send()` — always prime with `next()` before the first send
    - Generators are single-use; call a generator *function* again to reset
