# :material-function-variant: Day 21 — functools, operator & itertools

!!! abstract "Day at a Glance"
    **Goal:** Master Python's three functional-programming standard-library modules — `functools`, `operator`, and `itertools` — and compose them into elegant data-processing pipelines.
    **C++ Equivalent:** Day 21 of Learn-Modern-CPP-OOP-30-Days (`std::accumulate`, `std::transform`, function objects, `std::ranges`)
    **Estimated Time:** 60–90 minutes

<div class="grid cards" markdown>
- :material-lightbulb-on: **Core Concept** — Compose small, pure functions into pipelines instead of writing imperative loops
- :material-snake: **Python Way** — `functools.reduce` + `itertools` iterators + `operator` helpers = expressive, lazy pipelines
- :material-alert: **Watch Out** — `itertools` returns lazy iterators — consuming them twice yields nothing the second time
- :material-check-circle: **By End of Day** — Build a `compose()` function, a `groupby` aggregation, and a `singledispatch` overloader
</div>

---

## :material-lightbulb-on: Intuition

!!! info "Core Idea"
    Functional programming treats computation as the evaluation of mathematical functions.
    Python's standard library provides three modules that enable this style without any third-party
    dependencies: `functools` supplies higher-order functions and caching; `operator` provides
    callable wrappers for Python operators (avoiding `lambda x: x.name` boilerplate); `itertools`
    delivers a collection of fast, memory-efficient iterators modelled on Haskell and APL.
    Together they let you express data transformations as declarative pipelines.

!!! success "Python vs C++"
    | Python | C++ equivalent |
    |---|---|
    | `functools.reduce(f, it, init)` | `std::accumulate(begin, end, init, f)` |
    | `functools.partial(f, x)` | `std::bind(f, x, _1)` |
    | `functools.lru_cache` | Manual memoisation map |
    | `operator.itemgetter(k)` | Lambda `[k](auto& m){ return m[k]; }` |
    | `itertools.chain(*its)` | Range concatenation |
    | `itertools.product(a, b)` | Nested `for` loops |
    | `itertools.accumulate(it, f)` | Prefix scan with `std::inclusive_scan` |
    | `singledispatch` | `if constexpr` / `std::variant` + `std::visit` |

---

## :material-pipe-valve: Functional Pipeline Composition

```mermaid
flowchart LR
    RAW([Raw iterable]) --> F1[filter / takewhile]
    F1 --> F2[map / starmap]
    F2 --> F3[groupby / chain]
    F3 --> F4[accumulate / reduce]
    F4 --> OUT([Result])

    style RAW fill:#1e3a5f,color:#fff
    style OUT fill:#1e5f3a,color:#fff
```

---

## :material-book-open-variant: Lesson

### `functools` — Higher-Order Functions

#### `reduce` and `compose`

```python
from functools import reduce
from typing import Callable, TypeVar

T = TypeVar("T")

# reduce: fold a sequence into a single value
total = reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5], 0)   # 15
product = reduce(lambda acc, x: acc * x, range(1, 6), 1)       # 120  (5!)


# compose: build a pipeline of unary functions (right-to-left, like math)
def compose(*fns: Callable) -> Callable:
    """compose(f, g, h)(x) == f(g(h(x)))"""
    return reduce(lambda f, g: lambda x: f(g(x)), fns)


normalize = compose(
    str.strip,
    str.lower,
    lambda s: s.replace("-", "_"),
)
print(normalize("  Hello-World  "))   # hello_world


# pipe: left-to-right version (more readable for data pipelines)
def pipe(*fns: Callable) -> Callable:
    return reduce(lambda f, g: lambda x: g(f(x)), fns)

pipeline = pipe(str.strip, str.upper, lambda s: f"[{s}]")
print(pipeline("  hello  "))          # [HELLO]
```

#### `partial` — Freeze Arguments

```python
from functools import partial

def power(base: float, exp: float) -> float:
    return base ** exp

square = partial(power, exp=2)
cube   = partial(power, exp=3)

print(square(5))   # 25.0
print(cube(3))     # 27.0

# Common use: pre-fill a print separator
print_tab = partial(print, sep="\t")
print_tab("Name", "Age", "Score")     # Name	Age	Score
```

#### `lru_cache` — Memoisation

```python
from functools import lru_cache

@lru_cache(maxsize=None)   # unbounded cache (use None for pure maths)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))             # instant
print(fib.cache_info())    # CacheInfo(hits=48, misses=51, maxsize=None, currsize=51)
fib.cache_clear()          # reset the cache


# Python 3.9+: @cache is lru_cache(maxsize=None) with less overhead
from functools import cache

@cache
def factorial(n: int) -> int:
    return 1 if n == 0 else n * factorial(n - 1)
```

#### `total_ordering` — Fill in Comparison Methods

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other: "Version") -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

# total_ordering fills in <=, >, >= automatically
v1 = Version(1, 2, 3)
v2 = Version(2, 0, 0)
print(v1 < v2)    # True
print(v2 >= v1)   # True
```

#### `singledispatch` — Type-Based Overloading

```python
from functools import singledispatch

@singledispatch
def serialize(value: object) -> str:
    raise NotImplementedError(f"Cannot serialize {type(value)}")

@serialize.register(int)
@serialize.register(float)
def _serialize_number(value: int | float) -> str:
    return str(value)

@serialize.register(list)
def _serialize_list(value: list) -> str:
    return "[" + ", ".join(serialize(item) for item in value) + "]"

@serialize.register(dict)
def _serialize_dict(value: dict) -> str:
    pairs = ", ".join(f"{k!r}: {serialize(v)}" for k, v in value.items())
    return "{" + pairs + "}"

@serialize.register(str)
def _serialize_str(value: str) -> str:
    return repr(value)

print(serialize(42))                        # 42
print(serialize([1, "hi", 3.14]))          # [1, 'hi', 3.14]
print(serialize({"x": [1, 2]}))           # {'x': [1, 2]}
```

---

### `operator` — Callable Operator Wrappers

```python
import operator

# Avoid lambda boilerplate with attrgetter, itemgetter, methodcaller
from operator import attrgetter, itemgetter, methodcaller
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    department: str
    salary: float

employees = [
    Employee("Alice", "Engineering", 95_000),
    Employee("Bob", "Marketing", 72_000),
    Employee("Carol", "Engineering", 110_000),
    Employee("Dave", "Marketing", 68_000),
]

# Sort by salary descending
top_earners = sorted(employees, key=attrgetter("salary"), reverse=True)
print([e.name for e in top_earners])   # ['Carol', 'Alice', 'Bob', 'Dave']

# Sort by department then salary
sorted_emp = sorted(employees, key=attrgetter("department", "salary"))

# itemgetter works on sequences and mappings
records = [{"name": "Alice", "score": 90}, {"name": "Bob", "score": 85}]
by_score = sorted(records, key=itemgetter("score"), reverse=True)

# methodcaller: call a method by name
words = ["banana", "apple", "cherry"]
upper_words = list(map(methodcaller("upper"), words))   # ['BANANA', 'APPLE', 'CHERRY']

# Operator functions for reduce
from functools import reduce
import operator

values = [2, 3, 4, 5]
print(reduce(operator.mul, values))       # 120   (2*3*4*5)
print(reduce(operator.add, values))       # 14
print(reduce(operator.or_, [{1, 2}, {2, 3}, {4}]))  # {1, 2, 3, 4}
```

---

### `itertools` — Lazy Iterator Building Blocks

#### Infinite Iterators

```python
import itertools

# count(start, step)
for i in itertools.islice(itertools.count(10, 5), 5):
    print(i, end=" ")   # 10 15 20 25 30

# cycle(iterable) — repeat forever
spinner = itertools.cycle(["⠋", "⠙", "⠹", "⠸"])
frames = list(itertools.islice(spinner, 8))
print(frames)   # ['⠋', '⠙', '⠹', '⠸', '⠋', '⠙', '⠹', '⠸']

# repeat(value, times)
padded = list(itertools.repeat(0, 5))   # [0, 0, 0, 0, 0]
```

#### Combinatoric Iterators

```python
# product — Cartesian product (nested loops)
for suit, rank in itertools.product(["♠", "♥"], ["A", "K", "Q"]):
    print(f"{rank}{suit}", end=" ")
# A♠ K♠ Q♠ A♥ K♥ Q♥

# combinations and permutations
from itertools import combinations, permutations
print(list(combinations("ABC", 2)))    # [('A','B'),('A','C'),('B','C')]
print(list(permutations("AB", 2)))     # [('A','B'),('B','A')]
```

#### Slicing and Chaining

```python
import itertools

# chain — flatten iterables
merged = list(itertools.chain([1, 2], [3, 4], [5]))   # [1, 2, 3, 4, 5]
flat   = list(itertools.chain.from_iterable([[1, 2], [3, 4]]))  # [1, 2, 3, 4]

# islice — lazy slice without materialising
first_ten_evens = list(itertools.islice(itertools.count(0, 2), 10))
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# takewhile / dropwhile
data = [1, 3, 5, 2, 7, 9]
print(list(itertools.takewhile(lambda x: x % 2 == 1, data)))   # [1, 3, 5]
print(list(itertools.dropwhile(lambda x: x % 2 == 1, data)))   # [2, 7, 9]
```

#### `accumulate` — Running Totals and Scans

```python
import itertools
import operator

sales = [120, 85, 200, 150, 90, 175]

# Running sum
running = list(itertools.accumulate(sales))
print(running)   # [120, 205, 405, 555, 645, 820]

# Running maximum
running_max = list(itertools.accumulate(sales, max))
print(running_max)   # [120, 120, 200, 200, 200, 200]

# Running product
running_prod = list(itertools.accumulate(range(1, 6), operator.mul))
print(running_prod)   # [1, 2, 6, 24, 120]  (factorials)

# With initial value (Python 3.8+)
running_sum = list(itertools.accumulate(sales, operator.add, initial=0))
print(running_sum)   # [0, 120, 205, 405, 555, 645, 820]
```

#### `groupby` — Aggregation

```python
import itertools
from operator import attrgetter
from dataclasses import dataclass

@dataclass
class Sale:
    product: str
    region: str
    amount: float

sales = [
    Sale("Widget", "North", 100),
    Sale("Gadget", "North", 200),
    Sale("Widget", "South", 150),
    Sale("Gadget", "South", 300),
    Sale("Widget", "North", 50),
]

# groupby requires the data to be SORTED by the key first
sales_sorted = sorted(sales, key=attrgetter("region", "product"))

totals: dict[str, dict[str, float]] = {}
for region, group in itertools.groupby(sales_sorted, key=attrgetter("region")):
    totals[region] = {}
    for product, sub_group in itertools.groupby(group, key=attrgetter("product")):
        totals[region][product] = sum(s.amount for s in sub_group)

import pprint
pprint.pprint(totals)
# {'North': {'Gadget': 200.0, 'Widget': 150.0},
#  'South': {'Gadget': 300.0, 'Widget': 150.0}}
```

#### Full Functional Pipeline

```python
import itertools
from functools import reduce, partial
from operator import attrgetter

# Goal: find the top-3 revenue products across all regions

def pipeline(data):
    # Step 1: group by product
    by_product = sorted(data, key=attrgetter("product"))
    product_totals = {
        product: sum(s.amount for s in group)
        for product, group in itertools.groupby(by_product, key=attrgetter("product"))
    }
    # Step 2: sort descending, take top 3
    top3 = list(itertools.islice(
        sorted(product_totals.items(), key=lambda kv: kv[1], reverse=True),
        3
    ))
    return top3

print(pipeline(sales))   # [('Gadget', 500.0), ('Widget', 300.0)]
```

---

## :material-alert: Common Pitfalls

!!! warning "`itertools` Iterators Are Exhaustible"
    ```python
    gen = itertools.chain([1, 2], [3, 4])
    print(list(gen))   # [1, 2, 3, 4]
    print(list(gen))   # []  ← already exhausted!

    # Fix: materialise with list() if you need to iterate multiple times,
    # or recreate the iterator expression each time.
    ```

!!! warning "`groupby` Requires Pre-Sorted Input"
    ```python
    data = [("B", 1), ("A", 2), ("B", 3)]
    # Without sorting: groupby sees A and B as separate groups
    for k, g in itertools.groupby(data, key=lambda x: x[0]):
        print(k, list(g))
    # B [('B', 1)]
    # A [('A', 2)]
    # B [('B', 3)]   ← 'B' appears TWICE — wrong!

    # Fix: sort first
    for k, g in itertools.groupby(sorted(data, key=lambda x: x[0]), key=lambda x: x[0]):
        print(k, list(g))
    ```

!!! danger "`lru_cache` on Methods Leaks Memory"
    ```python
    class Foo:
        @lru_cache(maxsize=128)
        def compute(self, x): ...

    # The cache holds a reference to 'self' (as part of the cache key),
    # preventing garbage collection. Use functools.cached_property instead,
    # or apply lru_cache at the module level to a free function.
    ```

!!! danger "`singledispatch` Dispatches on the FIRST Argument Only"
    ```python
    @singledispatch
    def process(a, b): ...

    @process.register(int)
    def _(a, b): ...       # dispatches on type of 'a', ignores type of 'b'

    # For multi-argument dispatch, use a dict lookup or methoddispatch patterns.
    ```

---

## :material-help-circle: Flashcards

???+ question "What is the difference between `compose` and `pipe` in functional programming?"
    Both chain functions together, but in opposite directions.
    `compose(f, g, h)(x)` = `f(g(h(x)))` — right-to-left (mathematical notation).
    `pipe(f, g, h)(x)` = `h(g(f(x)))` — left-to-right (data flow / shell pipe notation).
    Python's `functools.reduce` implements both depending on the order you pass functions.

???+ question "Why should you use `operator.attrgetter` instead of `lambda x: x.name`?"
    `attrgetter` is faster (implemented in C), supports dotted attribute paths (`attrgetter("address.city")`),
    and can extract multiple attributes at once (`attrgetter("first", "last")` returns a tuple).
    It also has a clear, self-documenting name that communicates intent better than an anonymous lambda.

???+ question "How does `itertools.groupby` differ from SQL `GROUP BY`?"
    SQL `GROUP BY` works on the entire dataset and sorts internally.
    `itertools.groupby` is **lazy** and processes the iterable in a single pass — it only groups
    **consecutive** equal keys. You must sort by the key first to get SQL-like grouping semantics.
    The advantage is O(1) memory for streaming data; the requirement is that the input is sorted.

???+ question "When should you prefer `functools.cache` over `functools.lru_cache(maxsize=None)`?"
    `functools.cache` (Python 3.9+) is semantically identical to `lru_cache(maxsize=None)` but
    has a smaller memory footprint because it omits the doubly-linked list used to track LRU order
    (pointless when there is no eviction). Use `cache` for pure mathematical functions where you
    want to memoize everything; use `lru_cache` with a finite `maxsize` when you need to bound memory.

---

## :material-clipboard-check: Self Test

=== "Question 1"
    Use `itertools.accumulate` and `operator.mul` to compute a list of running factorials
    `[1!, 2!, 3!, 4!, 5!]` starting from 1, without any explicit loop or `math.factorial`.

=== "Answer 1"
    ```python
    import itertools
    import operator

    factorials = list(itertools.accumulate(range(1, 6), operator.mul))
    print(factorials)   # [1, 2, 6, 24, 120]

    # With initial value so index 0 = 0! = 1
    factorials_with_zero = list(
        itertools.accumulate(range(1, 6), operator.mul, initial=1)
    )
    print(factorials_with_zero)   # [1, 1, 2, 6, 24, 120]
    ```

=== "Question 2"
    Write a `compose` function using `functools.reduce` and use it to build a text-normalisation
    pipeline: strip whitespace, lower-case, replace spaces with underscores, then truncate to
    20 characters. Apply it to `"  Hello Beautiful World  "`.

=== "Answer 2"
    ```python
    from functools import reduce
    from typing import Callable

    def compose(*fns: Callable) -> Callable:
        return reduce(lambda f, g: lambda x: f(g(x)), fns)

    normalize = compose(
        lambda s: s[:20],                  # truncate  (applied last)
        lambda s: s.replace(" ", "_"),     # spaces -> underscores
        str.lower,                         # lower-case
        str.strip,                         # strip whitespace (applied first)
    )

    result = normalize("  Hello Beautiful World  ")
    print(result)   # hello_beautiful_wor   (20 chars)

    # Equivalent pipe (left-to-right, arguably more readable):
    def pipe(*fns: Callable) -> Callable:
        return reduce(lambda f, g: lambda x: g(f(x)), fns)

    normalize2 = pipe(
        str.strip,
        str.lower,
        lambda s: s.replace(" ", "_"),
        lambda s: s[:20],
    )
    print(normalize2("  Hello Beautiful World  "))   # hello_beautiful_wor
    ```

---

## :material-check-circle: Summary

!!! success "Key Takeaways"
    - `functools.reduce` folds a sequence into one value and powers both `compose` (right-to-left) and `pipe` (left-to-right) combinators.
    - `functools.partial` freezes arguments to create specialised callables without lambdas.
    - `functools.lru_cache` / `cache` memoize pure functions in one decorator line; `cache_info()` exposes hit rates.
    - `functools.singledispatch` provides type-based function overloading dispatching on the first argument.
    - `operator.attrgetter`, `itemgetter`, and `methodcaller` are faster, more expressive alternatives to boilerplate lambdas.
    - `itertools` delivers lazy, memory-efficient iterators: `chain`, `islice`, `takewhile`, `dropwhile`, `product`, `groupby`, and `accumulate` cover the vast majority of data-pipeline needs.
    - `groupby` **requires pre-sorted input** — always sort by the key first.
    - `itertools` iterators are **one-shot** — materialise with `list()` if you need to iterate more than once.
