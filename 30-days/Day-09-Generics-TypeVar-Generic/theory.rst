Day 09 — Generics: TypeVar and Generic
========================================

TypeVar and Generic[T]
-----------------------

.. code-block:: python

    from typing import TypeVar, Generic

    T = TypeVar("T")

    class Stack(Generic[T]):
        def __init__(self) -> None:
            self._items: list[T] = []

        def push(self, item: T) -> None:
            self._items.append(item)

        def pop(self) -> T:
            return self._items.pop()

    stack: Stack[int] = Stack()   # type-safe; mypy enforces T=int

TypeVar creates a placeholder that mypy/pyright resolves at each call site.
``Generic[T]`` makes the class parametrisable.  Python 3.12+ supports
``class Stack[T]:`` syntax directly.


Bounded TypeVar
----------------

.. code-block:: python

    class Comparable(Protocol):
        def __lt__(self, other) -> bool: ...

    C = TypeVar("C", bound="Comparable")

    def find_min(items: list[C]) -> C:
        return min(items)

``bound=X`` restricts T to subtypes of X.  The function body can use
operations that X supports.  C++ equivalent: ``template<typename T>
requires Comparable<T>``.


@overload — Multiple Signatures
---------------------------------

.. code-block:: python

    from typing import overload

    @overload
    def process(value: int) -> str: ...
    @overload
    def process(value: str) -> int: ...

    def process(value: int | str) -> str | int:   # actual implementation
        if isinstance(value, int): return str(value)
        return int(value)

``@overload`` stubs are for the type checker only.  The actual
implementation (without ``@overload``) handles all cases.


ParamSpec — Decorator Type Safety
-----------------------------------

.. code-block:: python

    from typing import ParamSpec, Callable, TypeVar

    P = ParamSpec("P")
    T = TypeVar("T")

    def logged(f: Callable[P, T]) -> Callable[P, T]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            print(f"calling {f.__name__}")
            return f(*args, **kwargs)
        return wrapper

``ParamSpec`` captures the parameter specification of a callable, so the
decorated function's type signature is preserved for type checkers.


Python vs C++ Generics
------------------------

+--------------------+--------------------------------+-------------------------------+
| Feature            | C++ Templates                  | Python Generics               |
+====================+================================+===============================+
| Evaluation         | Compile-time instantiation     | Runtime (type erasure)        |
+--------------------+--------------------------------+-------------------------------+
| Type checking      | At instantiation               | Via mypy/pyright              |
+--------------------+--------------------------------+-------------------------------+
| Syntax             | ``template<typename T>``       | ``TypeVar + Generic[T]``      |
+--------------------+--------------------------------+-------------------------------+
| Bounds/constraints | Concepts (C++20)               | ``bound=`` or Protocol        |
+--------------------+--------------------------------+-------------------------------+
| Runtime cost       | Zero (specialised code)        | None (same bytecode)          |
+--------------------+--------------------------------+-------------------------------+

Python generics are purely for static analysis — at runtime, ``Stack[int]``
and ``Stack[str]`` are the same class.
