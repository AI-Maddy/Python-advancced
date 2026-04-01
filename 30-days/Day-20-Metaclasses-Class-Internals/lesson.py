"""
Day 20 — Metaclasses & Class Internals
========================================
Topics:
  - type(name, bases, namespace) — classes are objects
  - __new__ vs __init__ on metaclasses
  - SingletonMeta, RegistryMeta implementations
  - __prepare__ for ordered namespace
  - __init_subclass__ as lightweight alternative
  - vars(), dir(), getattr(), setattr()
"""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, ClassVar


# ===========================================================================
# 1. Classes are objects — type() as factory
# ===========================================================================

def demo_type_as_class_factory() -> None:
    """
    type(name, bases, namespace) creates a class dynamically.
    This is equivalent to the 'class' keyword at runtime.
    """

    # Manual class creation via type()
    MyClass = type(
        "MyClass",            # class name
        (object,),            # base classes (tuple)
        {                     # class namespace (attributes, methods)
            "greeting": "Hello",
            "greet": lambda self: f"{self.greeting}, I am {type(self).__name__}",
        },
    )

    obj = MyClass()
    print(f"type(MyClass) = {type(MyClass)}")   # <class 'type'>
    print(f"type(obj) = {type(obj)}")           # <class '__main__.MyClass'>
    print(obj.greet())

    # The 'class' keyword is syntactic sugar for the above
    class Equivalent:
        greeting = "Hello"
        def greet(self) -> str:
            return f"{self.greeting}, I am {type(self).__name__}"

    print(f"Both are type: {type(MyClass) is type(Equivalent)}")


# ===========================================================================
# 2. Metaclass lifecycle: __prepare__ → __new__ → __init__
# ===========================================================================

class TracingMeta(type):
    """Metaclass that prints each lifecycle step."""

    @classmethod
    def __prepare__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Called FIRST — returns the namespace dict that will hold class body.
        Use OrderedDict here to track definition order.
        """
        print(f"__prepare__: building namespace for '{name}'")
        return OrderedDict()

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> TracingMeta:
        """
        Called SECOND — actually creates and returns the class object.
        Modify namespace here before class is finalised.
        """
        print(f"__new__: creating class '{name}'")
        return super().__new__(mcs, name, bases, dict(namespace))

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> None:
        """Called THIRD — initialise the class object (already created)."""
        print(f"__init__: initialising class '{name}'")
        super().__init__(name, bases, namespace)


class TracedClass(metaclass=TracingMeta):
    """This class is created via TracingMeta."""
    x: int = 10
    def method(self) -> int:
        return self.x


# ===========================================================================
# 3. SingletonMeta
# ===========================================================================

class SingletonMeta(type):
    """
    Metaclass that ensures only one instance per class is ever created.

    >>> class Config(metaclass=SingletonMeta): pass
    >>> Config() is Config()
    True
    """

    _instances: ClassVar[dict[type, Any]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Intercept instance creation; return cached instance if present."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppSettings(metaclass=SingletonMeta):
    """Application-wide settings — singleton."""

    def __init__(self) -> None:
        self.theme: str = "light"
        self.language: str = "en"


# ===========================================================================
# 4. RegistryMeta — automatic subclass registration
# ===========================================================================

class RegistryMeta(type):
    """
    Metaclass that keeps a registry of all concrete subclasses.
    Abstract base classes (those with name starting with '_') are excluded.
    """

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> None:
        super().__init__(name, bases, namespace)
        # Attach _registry to the root class
        if not hasattr(cls, "_registry"):
            cls._registry: dict[str, type] = {}
        elif not name.startswith("_"):
            cls._registry[name] = cls

    @classmethod
    def get(mcs, cls: type, name: str) -> type:
        """Retrieve a registered subclass by name."""
        return cls._registry[name]


class _Command(metaclass=RegistryMeta):
    """Abstract base for commands — excluded from registry (leading _)."""

    def execute(self) -> str:
        raise NotImplementedError


class PrintCommand(_Command):
    """Prints something."""

    def execute(self) -> str:
        return "Printing..."


class SaveCommand(_Command):
    """Saves something."""

    def execute(self) -> str:
        return "Saving..."


# ===========================================================================
# 5. __prepare__ for ordered attribute tracking
# ===========================================================================

class OrderedMeta(type):
    """
    Tracks the definition order of class attributes (useful for ORMs, forms).
    """

    @classmethod
    def __prepare__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        **kwargs: Any,
    ) -> OrderedDict[str, Any]:
        return OrderedDict()

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: OrderedDict[str, Any],
        **kwargs: Any,
    ) -> OrderedMeta:
        cls = super().__new__(mcs, name, bases, dict(namespace))
        # Store definition order of non-dunder attributes
        cls._field_order: list[str] = [
            k for k in namespace if not k.startswith("__")
        ]
        return cls


class FormDefinition(metaclass=OrderedMeta):
    """HTML form with ordered fields."""
    username: str = ""
    email: str = ""
    password: str = ""


# ===========================================================================
# 6. __init_subclass__ — lightweight alternative to metaclasses
# ===========================================================================

class Plugin:
    """
    Base class using __init_subclass__ to auto-register plugins.
    Simpler than RegistryMeta for most use cases.
    """

    _plugins: ClassVar[dict[str, type[Plugin]]] = {}

    def __init_subclass__(cls, name: str = "", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if name:
            Plugin._plugins[name] = cls

    @classmethod
    def get_plugin(cls, name: str) -> type[Plugin]:
        """Return plugin class by name."""
        return cls._plugins[name]

    def run(self) -> str:
        """Override in subclasses."""
        raise NotImplementedError


class CsvPlugin(Plugin, name="csv"):
    """CSV output plugin."""

    def run(self) -> str:
        return "Writing CSV..."


class JsonPlugin(Plugin, name="json"):
    """JSON output plugin."""

    def run(self) -> str:
        return "Writing JSON..."


# ===========================================================================
# 7. vars(), dir(), getattr(), setattr() introspection
# ===========================================================================

def introspect(obj: Any) -> None:
    """Print key introspection data about an object."""
    print(f"\n--- Introspecting {type(obj).__name__} ---")
    print(f"vars(): {list(vars(obj).keys())}")
    # dir() includes inherited names
    public = [n for n in dir(obj) if not n.startswith("_")]
    print(f"dir() (public): {public[:10]}...")
    print(f"getattr(obj, 'theme'): {getattr(obj, 'theme', '<missing>')}")

    # Dynamic attribute set
    setattr(obj, "dynamic_attr", 42)
    print(f"After setattr: obj.dynamic_attr = {obj.dynamic_attr}")


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 20 — Metaclasses & Class Internals")
    print("=" * 60)

    print("\n--- type() as factory ---")
    demo_type_as_class_factory()

    print("\n--- TracingMeta lifecycle ---")
    # TracedClass was already created at module load — output already printed.
    # Create an instance to show it works normally:
    obj = TracedClass()
    print(f"TracedClass().x = {obj.method()}")

    print("\n--- SingletonMeta ---")
    s1 = AppSettings()
    s2 = AppSettings()
    s1.theme = "dark"
    print(f"s1 is s2: {s1 is s2}")
    print(f"s2.theme: {s2.theme}")  # "dark" — same object

    print("\n--- RegistryMeta ---")
    print(f"Registry: {list(_Command._registry.keys())}")
    cmd = _Command._registry["PrintCommand"]()
    print(f"PrintCommand.execute(): {cmd.execute()}")

    print("\n--- OrderedMeta ---")
    print(f"FormDefinition field order: {FormDefinition._field_order}")

    print("\n--- __init_subclass__ plugin registry ---")
    print(f"Plugins: {list(Plugin._plugins.keys())}")
    plugin = Plugin.get_plugin("json")()
    print(f"JsonPlugin.run(): {plugin.run()}")

    print("\n--- Introspection ---")
    settings = AppSettings()
    introspect(settings)
