"""
Tests for Day 29 — Advanced Topics Deep Dive
Run with: pytest tests/test_day29.py -v
"""
from __future__ import annotations

import copy
import gc
import pickle
import threading
import weakref
from collections import ChainMap, Counter, OrderedDict, deque
from enum import Enum, Flag, IntEnum, auto
from pathlib import Path
from typing import Any

import pytest


# ---------------------------------------------------------------------------
# __slots__ inheritance
# ---------------------------------------------------------------------------

class Base:
    __slots__ = ("x",)
    def __init__(self, x: int) -> None:
        self.x = x


class Slotted(Base):
    __slots__ = ("y",)
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x)
        self.y = y


class Unslotted(Base):
    def __init__(self, x: int, z: int) -> None:
        super().__init__(x)
        self.z = z


def test_slotted_child_no_dict() -> None:
    obj = Slotted(1, 2)
    assert not hasattr(obj, "__dict__")


def test_unslotted_child_has_dict() -> None:
    obj = Unslotted(1, 3)
    assert hasattr(obj, "__dict__")


def test_slotted_attributes_work() -> None:
    obj = Slotted(10, 20)
    assert obj.x == 10
    assert obj.y == 20


def test_slotted_prevents_new_attributes() -> None:
    obj = Slotted(1, 2)
    with pytest.raises(AttributeError):
        obj.z = 99  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# __missing__
# ---------------------------------------------------------------------------

class CountingDict(dict):
    def __missing__(self, key: object) -> int:
        return 0


def test_missing_returns_default() -> None:
    d = CountingDict()
    d["hits"] = 5
    assert d["hits"] == 5
    assert d["misses"] == 0   # missing key → 0


def test_missing_does_not_store() -> None:
    d = CountingDict()
    _ = d["x"]
    assert "x" not in d   # __missing__ returned value but didn't store it


# ---------------------------------------------------------------------------
# ChainMap
# ---------------------------------------------------------------------------

def test_chainmap_priority() -> None:
    defaults   = {"a": 1, "b": 2}
    overrides  = {"b": 99}
    cm = ChainMap(overrides, defaults)
    assert cm["a"] == 1    # from defaults
    assert cm["b"] == 99   # overrides wins


def test_chainmap_new_child() -> None:
    base = ChainMap({"x": 10})
    child = base.new_child({"x": 99, "y": 20})
    assert child["x"] == 99
    assert child["y"] == 20
    assert base["x"] == 10  # parent unchanged


# ---------------------------------------------------------------------------
# Counter
# ---------------------------------------------------------------------------

def test_counter_most_common() -> None:
    c = Counter("aababc")
    top = c.most_common(1)
    assert top[0][0] == "a"
    assert top[0][1] == 3


def test_counter_arithmetic() -> None:
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2)
    assert (c1 + c2)["a"] == 4
    assert (c1 - c2)["b"] == 0   # 1-2 < 0 → not kept


# ---------------------------------------------------------------------------
# deque
# ---------------------------------------------------------------------------

def test_deque_maxlen_eviction() -> None:
    dq = deque([1, 2, 3], maxlen=3)
    dq.append(4)
    assert list(dq) == [2, 3, 4]   # 1 evicted


def test_deque_rotate() -> None:
    dq = deque([1, 2, 3, 4])
    dq.rotate(1)
    assert list(dq) == [4, 1, 2, 3]


# ---------------------------------------------------------------------------
# weakref
# ---------------------------------------------------------------------------

class Obj:
    pass


def test_weakref_alive() -> None:
    obj = Obj()
    ref = weakref.ref(obj)
    assert ref() is obj


def test_weakref_after_del() -> None:
    obj = Obj()
    ref = weakref.ref(obj)
    del obj
    gc.collect()
    assert ref() is None


def test_weak_value_dict() -> None:
    d: weakref.WeakValueDictionary[str, Obj] = weakref.WeakValueDictionary()
    obj = Obj()
    d["key"] = obj
    assert "key" in d
    del obj
    gc.collect()
    assert "key" not in d


# ---------------------------------------------------------------------------
# copy
# ---------------------------------------------------------------------------

class Box:
    def __init__(self, contents: list[int]) -> None:
        self.contents = contents


def test_shallow_copy_shares_contents() -> None:
    b = Box([1, 2, 3])
    b_copy = copy.copy(b)
    assert b_copy is not b
    assert b_copy.contents is b.contents   # same list object


def test_deep_copy_independent() -> None:
    b = Box([1, 2, 3])
    b_deep = copy.deepcopy(b)
    assert b_deep.contents is not b.contents
    b_deep.contents.append(99)
    assert 99 not in b.contents


# ---------------------------------------------------------------------------
# pickle
# ---------------------------------------------------------------------------

class Config:
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value
        self._lock = threading.Lock()

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self._lock = threading.Lock()


def test_pickle_round_trip() -> None:
    cfg = Config("db", "localhost:5432")
    data = pickle.dumps(cfg)
    loaded = pickle.loads(data)
    assert loaded.name == "db"
    assert loaded.value == "localhost:5432"


def test_pickle_reinitialises_lock() -> None:
    cfg = Config("x", "y")
    loaded = pickle.loads(pickle.dumps(cfg))
    assert hasattr(loaded, "_lock")
    assert isinstance(loaded._lock, type(threading.Lock()))


# ---------------------------------------------------------------------------
# enum
# ---------------------------------------------------------------------------

class Season(Enum):
    SPRING = auto()
    SUMMER = auto()
    AUTUMN = auto()
    WINTER = auto()


class Access(Flag):
    NONE  = 0
    READ  = auto()
    WRITE = auto()


class Code(IntEnum):
    OK    = 200
    ERROR = 500


def test_enum_member_name() -> None:
    assert Season.SPRING.name == "SPRING"


def test_enum_iteration() -> None:
    names = [s.name for s in Season]
    assert "SPRING" in names and "WINTER" in names


def test_flag_combine() -> None:
    rw = Access.READ | Access.WRITE
    assert Access.READ in rw
    assert Access.WRITE in rw


def test_intenum_comparable_to_int() -> None:
    assert Code.OK == 200
    assert Code.ERROR > 300


# ---------------------------------------------------------------------------
# pathlib
# ---------------------------------------------------------------------------

def test_path_write_read(tmp_path: Path) -> None:
    f = tmp_path / "test.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"


def test_path_properties(tmp_path: Path) -> None:
    f = tmp_path / "data.csv"
    assert f.name == "data.csv"
    assert f.stem == "data"
    assert f.suffix == ".csv"
    assert f.parent == tmp_path


def test_path_glob(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "c.py").write_text("c")
    txt_files = list(tmp_path.glob("*.txt"))
    assert len(txt_files) == 2
