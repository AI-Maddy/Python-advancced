"""
Day 29 — Advanced Topics Deep Dive
=====================================
Topics:
  - __slots__ with inheritance edge cases
  - __missing__ on dict subclasses
  - collections.ChainMap, Counter, deque, OrderedDict
  - weakref.ref and WeakValueDictionary
  - copy.copy vs copy.deepcopy with __copy__/__deepcopy__
  - pickle protocol: __getstate__/__setstate__
  - enum.Enum, IntEnum, Flag, auto()
  - pathlib.Path operations
"""
from __future__ import annotations

import copy
import pickle
import weakref
from collections import ChainMap, Counter, OrderedDict, deque
from enum import Enum, Flag, IntEnum, auto
from pathlib import Path
from typing import Any


# ===========================================================================
# 1. __slots__ with inheritance edge cases
# ===========================================================================

class Base:
    """Base with __slots__ — no __dict__."""
    __slots__ = ("x",)

    def __init__(self, x: int) -> None:
        self.x = x


class Child(Base):
    """
    Child inherits __slots__ from Base.
    Adding more slots is fine.
    NOT adding __slots__ in Child causes a __dict__ to appear
    (the slot from Base is still there, but Child adds __dict__).
    """
    __slots__ = ("y",)  # extend, don't re-define parent slots

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x)
        self.y = y


class ChildWithDict(Base):
    """
    No __slots__ → gets __dict__ in addition to parent's slots.
    Common footgun: you think it's all-slots but it's not.
    """
    # No __slots__ defined → __dict__ appears on instances

    def __init__(self, x: int, z: int) -> None:
        super().__init__(x)
        self.z = z   # stored in __dict__


def demo_slots_inheritance() -> None:
    c = Child(1, 2)
    print(f"Child slots: {c.__slots__}")
    print(f"Child has __dict__: {hasattr(c, '__dict__')}")   # False

    cd = ChildWithDict(1, 3)
    print(f"ChildWithDict has __dict__: {hasattr(cd, '__dict__')}")  # True
    print(f"ChildWithDict.__dict__: {cd.__dict__}")  # {z: 3}


# ===========================================================================
# 2. __missing__ on dict subclasses (defaultdict-like)
# ===========================================================================

class AutoVivify(dict):
    """
    Nested auto-creating dict.
    Accessing a missing key returns a new AutoVivify.
    """

    def __missing__(self, key: str) -> AutoVivify:
        """Called when __getitem__ fails to find a key."""
        self[key] = AutoVivify()
        return self[key]


class CountingDict(dict):
    """Returns 0 for missing integer keys."""

    def __missing__(self, key: object) -> int:
        """Return 0 for any unknown key."""
        return 0


def demo_missing() -> None:
    av = AutoVivify()
    av["a"]["b"]["c"] = 42    # no KeyError — keys auto-created
    print(f"AutoVivify: {dict(av)}")

    cd = CountingDict()
    cd["hits"] = 5
    print(f"CountingDict missing key: {cd['misses']}")  # 0


# ===========================================================================
# 3. collections
# ===========================================================================

def demo_collections() -> None:
    # --- ChainMap ---
    defaults   = {"color": "blue",  "font": "Arial", "size": 12}
    user_prefs = {"color": "green", "size": 14}
    theme = ChainMap(user_prefs, defaults)
    print(f"ChainMap color: {theme['color']}")  # green (user wins)
    print(f"ChainMap font:  {theme['font']}")   # Arial (from defaults)

    # New child scope
    child_scope = theme.new_child({"color": "red"})
    print(f"Child color: {child_scope['color']}")  # red

    # --- Counter ---
    words = "the cat sat on the mat the cat".split()
    counts = Counter(words)
    print(f"Counter: {counts.most_common(3)}")
    counts.update(["cat", "cat"])   # add more
    print(f"cat count: {counts['cat']}")

    # Arithmetic on counters
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=4)
    print(f"c1 + c2: {c1 + c2}")
    print(f"c1 - c2: {c1 - c2}")   # only positive counts

    # --- deque ---
    dq = deque(range(5), maxlen=5)
    dq.appendleft(99)   # pushes 4 off the right
    print(f"deque after appendleft(99): {dq}")
    dq.rotate(2)        # rotate right by 2
    print(f"after rotate(2): {dq}")

    # --- OrderedDict ---
    od = OrderedDict()
    od["a"] = 1
    od["b"] = 2
    od["c"] = 3
    od.move_to_end("a")   # move 'a' to the end
    print(f"OrderedDict after move_to_end('a'): {list(od.keys())}")


# ===========================================================================
# 4. weakref
# ===========================================================================

class Cache:
    """Simple object that can be garbage-collected."""
    def __init__(self, name: str) -> None:
        self.name = name
    def __repr__(self) -> str:
        return f"Cache({self.name!r})"


def demo_weakref() -> None:
    import gc

    obj = Cache("important_data")

    # weakref.ref — callable that returns obj or None if collected
    ref = weakref.ref(obj)
    print(f"Alive: {ref()}")       # Cache('important_data')

    del obj
    gc.collect()
    print(f"After del: {ref()}")   # None

    # WeakValueDictionary — values are weak references
    registry: weakref.WeakValueDictionary[str, Cache] = weakref.WeakValueDictionary()
    item = Cache("cached_item")
    registry["item"] = item
    print(f"Registry has item: {'item' in registry}")
    del item
    gc.collect()
    print(f"After del: {'item' in registry}")   # False — auto-removed


# ===========================================================================
# 5. copy.copy vs copy.deepcopy + __copy__/__deepcopy__
# ===========================================================================

class Node:
    """Linked list node with custom copy behaviour."""

    def __init__(self, value: int, next_node: Node | None = None) -> None:
        self.value = value
        self.next = next_node

    def __copy__(self) -> Node:
        """Shallow copy — same next pointer."""
        return Node(self.value, self.next)

    def __deepcopy__(self, memo: dict[int, Any]) -> Node:
        """Deep copy — recursively copy next."""
        new_node = Node(self.value)
        memo[id(self)] = new_node   # prevent infinite loops in cycles
        if self.next is not None:
            new_node.next = copy.deepcopy(self.next, memo)
        return new_node


def demo_copy() -> None:
    n2 = Node(2)
    n1 = Node(1, n2)

    shallow = copy.copy(n1)
    deep    = copy.deepcopy(n1)

    print(f"Original n1.next is n2: {n1.next is n2}")
    print(f"Shallow n1.next is n2:  {shallow.next is n2}")   # True — same object
    print(f"Deep    n1.next is n2:  {deep.next is n2}")       # False — new object


# ===========================================================================
# 6. pickle protocol: __getstate__ / __setstate__
# ===========================================================================

class SecretStore:
    """
    Stores a secret that should NOT be pickled.
    __getstate__/__setstate__ control what is serialized.
    """

    def __init__(self, data: str, secret: str) -> None:
        self.data = data
        self.secret = secret        # sensitive — exclude from pickle
        self._cache: dict[str, Any] = {}   # runtime cache — exclude too

    def __getstate__(self) -> dict[str, Any]:
        """Return picklable state (omit secret and cache)."""
        return {"data": self.data}

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Restore state; reinitialise excluded fields."""
        self.data = state["data"]
        self.secret = ""            # reset to empty on load
        self._cache = {}

    def __repr__(self) -> str:
        return f"SecretStore(data={self.data!r}, secret={'*' * len(self.secret)})"


def demo_pickle() -> None:
    store = SecretStore("public_data", "s3cr3t!")
    print(f"Original: {store}")

    pickled = pickle.dumps(store)
    loaded = pickle.loads(pickled)
    print(f"Loaded:   {loaded}")
    print(f"Secret lost: {loaded.secret!r}")   # "" — not pickled


# ===========================================================================
# 7. enum
# ===========================================================================

class Color(Enum):
    """Simple enum."""
    RED   = 1
    GREEN = 2
    BLUE  = 3

    def hex_code(self) -> str:
        """Custom method on enum member."""
        return {Color.RED: "#FF0000", Color.GREEN: "#00FF00", Color.BLUE: "#0000FF"}[self]


class Permission(Flag):
    """Bit-flag enum — supports bitwise operators."""
    NONE    = 0
    READ    = auto()
    WRITE   = auto()
    EXECUTE = auto()
    RWX     = READ | WRITE | EXECUTE


class HTTPStatus(IntEnum):
    """Comparable to ints."""
    OK        = 200
    NOT_FOUND = 404
    ERROR     = 500


def demo_enum() -> None:
    # Color
    c = Color.RED
    print(f"Color: {c.name} = {c.value}, hex={c.hex_code()}")
    print(f"Color.GREEN in Color: {Color.GREEN in Color}")

    # Flag — combine and test
    user_perms = Permission.READ | Permission.WRITE
    print(f"Permissions: {user_perms}")
    print(f"Can execute: {Permission.EXECUTE in user_perms}")
    print(f"Can read:    {Permission.READ in user_perms}")

    # IntEnum — comparable to int
    status = HTTPStatus.OK
    print(f"Status {status} == 200: {status == 200}")
    print(f"Status > 300: {status > 300}")


# ===========================================================================
# 8. pathlib.Path
# ===========================================================================

def demo_pathlib() -> None:
    p = Path("/tmp/day29_demo")
    p.mkdir(exist_ok=True)

    # Write and read
    file = p / "sample.txt"
    file.write_text("Hello from pathlib!\nLine 2\n")
    content = file.read_text()
    print(f"Read: {content.splitlines()}")

    # Path operations
    print(f"name:   {file.name}")
    print(f"stem:   {file.stem}")
    print(f"suffix: {file.suffix}")
    print(f"parent: {file.parent}")
    print(f"exists: {file.exists()}")

    # Glob
    txt_files = list(p.glob("*.txt"))
    print(f"txt files: {[f.name for f in txt_files]}")

    # Cleanup
    file.unlink()
    p.rmdir()


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 29 — Advanced Topics Deep Dive")
    print("=" * 60)

    print("\n--- __slots__ inheritance ---")
    demo_slots_inheritance()

    print("\n--- __missing__ ---")
    demo_missing()

    print("\n--- collections ---")
    demo_collections()

    print("\n--- weakref ---")
    demo_weakref()

    print("\n--- copy ---")
    demo_copy()

    print("\n--- pickle ---")
    demo_pickle()

    print("\n--- enum ---")
    demo_enum()

    print("\n--- pathlib ---")
    demo_pathlib()
