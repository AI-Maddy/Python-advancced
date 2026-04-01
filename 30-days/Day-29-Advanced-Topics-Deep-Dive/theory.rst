Day 29 — Advanced Topics Deep Dive
=====================================

``__slots__`` Inheritance
--------------------------

.. code-block:: python

    class Base:
        __slots__ = ("x",)   # no __dict__

    class Child(Base):
        __slots__ = ("y",)   # extends, does NOT re-declare parent slots

    class BadChild(Base):
        pass                 # no __slots__ → __dict__ appears (defeats the point)

``__missing__``
---------------

Called by ``dict.__getitem__`` when a key is absent.  More flexible than
``defaultdict`` because logic can be arbitrarily complex.

.. code-block:: python

    class AutoVivify(dict):
        def __missing__(self, key):
            self[key] = AutoVivify()
            return self[key]

collections
-----------

.. list-table::
   :header-rows: 1

   * - Class
     - Use Case
   * - ``ChainMap``
     - Layered config (CLI > env > defaults), nested scopes
   * - ``Counter``
     - Frequency counting, multiset arithmetic
   * - ``deque(maxlen=n)``
     - Efficient O(1) appendleft/popleft, sliding window
   * - ``OrderedDict``
     - Stable insertion order (regular dict is ordered in 3.7+, but OrderedDict has extra methods like ``move_to_end``)

weakref
-------

.. code-block:: python

    ref = weakref.ref(obj)   # returns obj or None after GC
    registry = weakref.WeakValueDictionary()   # auto-removes dead values

Use cases: caches that shouldn't keep objects alive, parent→child back-refs
in trees.

copy
----

.. code-block:: python

    shallow = copy.copy(obj)       # new outer object, shared inner objects
    deep    = copy.deepcopy(obj)   # fully independent copy of everything

Custom hooks:

.. code-block:: python

    def __copy__(self): ...       # shallow copy logic
    def __deepcopy__(self, memo): ...   # deep copy; use memo dict to handle cycles

pickle
------

.. code-block:: python

    data = pickle.dumps(obj)    # serialize
    obj  = pickle.loads(data)   # deserialize

Control what is serialized:

.. code-block:: python

    def __getstate__(self) -> dict: ...     # return picklable subset
    def __setstate__(self, state) -> None:  # restore + reinit non-picklable fields

enum
----

.. code-block:: python

    class Color(Enum):       # basic enum, value comparison
        RED = 1

    class Status(IntEnum):   # comparable to int
        OK = 200

    class Perm(Flag):        # bitwise combination
        READ = auto()
        WRITE = auto()

    user = Perm.READ | Perm.WRITE
    Perm.READ in user   # True

pathlib.Path
-------------

.. code-block:: python

    p = Path("/tmp/work")
    p.mkdir(parents=True, exist_ok=True)

    f = p / "data.txt"
    f.write_text("hello")
    content = f.read_text()

    f.name      # "data.txt"
    f.stem      # "data"
    f.suffix    # ".txt"
    f.parent    # Path("/tmp/work")

    list(p.glob("**/*.py"))    # recursive glob
    f.rename(p / "new.txt")
    f.unlink()                 # delete file
