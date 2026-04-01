Day 06 — Inheritance and Polymorphism
=======================================

Why This Day Matters
--------------------

Inheritance models "is-a" relationships and shares behaviour across a type
hierarchy.  Python's dispatch mechanism differs fundamentally from C++:
**all method calls use dynamic dispatch** — there is no non-virtual method.


Python vs C++ Polymorphism
----------------------------

+--------------------+-------------------------------------+-------------------------------+
| Feature            | C++                                 | Python                        |
+====================+=====================================+===============================+
| Virtual dispatch   | Opt-in with ``virtual``             | Always on                     |
+--------------------+-------------------------------------+-------------------------------+
| Override check     | ``override`` keyword (compile-time) | No check by default           |
+--------------------+-------------------------------------+-------------------------------+
| Slicing            | Silent when passing by value        | No slicing (everything is ref)|
+--------------------+-------------------------------------+-------------------------------+
| Pure virtual       | ``= 0``                             | Raise ``NotImplementedError`` |
+--------------------+-------------------------------------+-------------------------------+
| Abstract class     | Has ``= 0`` method                  | ``abc.ABC`` (Day 07)          |
+--------------------+-------------------------------------+-------------------------------+
| Multiple inherit.  | Complex (vtable per base)           | C3 MRO linearisation          |
+--------------------+-------------------------------------+-------------------------------+

Python has no vtable — attribute lookup traverses the MRO at runtime.


super() and the MRO
--------------------

.. code-block:: python

    class Square(Rectangle):
        def __init__(self, side: float) -> None:
            super().__init__(side, side)   # next in MRO: Rectangle.__init__

``super()`` does not mean "call the direct parent" — it means "call the next
class in the MRO chain".  This enables cooperative multiple inheritance.


C3 Linearisation (MRO)
------------------------

Python uses the C3 algorithm to build a consistent, monotonic linearisation
of the class hierarchy.  ``ClassName.__mro__`` shows the order::

    class Duck(Animal, Flyable, Swimmable):
        pass

    Duck.__mro__
    # (Duck, Animal, Flyable, Swimmable, object)

Rules:
1. A class always precedes its parents.
2. The order of listed parents is preserved.
3. Each class appears exactly once.


No Slicing Problem
-------------------

In C++, passing a derived object by value to a base-type parameter silently
discards the derived part ("slicing").  In Python, **everything is a reference**.
There is no slicing.

.. code-block:: python

    def process(shape: Shape) -> None:
        print(shape.area())    # always dispatches to correct subclass

    circle = Circle(5.0)
    process(circle)            # Circle.area() is called — no slicing


Mixin Pattern
--------------

Mixins add behaviour without modelling a true "is-a" relationship:

.. code-block:: python

    class JsonMixin:
        def to_json(self) -> str:
            import json
            return json.dumps({k: v for k, v in self.__dict__.items()
                                if not k.startswith("_")})

    class Product(JsonMixin, LogMixin):
        def __init__(self, name, price):
            self.name = name
            self.price = price

Guidelines for mixins:
- Mixin classes should not have ``__init__``.
- Mixins should use ``super()`` for cooperative inheritance.
- Name them with ``Mixin`` suffix for clarity.


Self-Check Questions
--------------------

**Q1: Why is there no slicing problem in Python?**

Python passes objects by reference, not by value.  Assigning a derived
object to a base-type variable just creates another reference to the same
object — no data is copied or discarded.

**Q2: What is cooperative multiple inheritance and when does** ``super()`` **matter?**

Cooperative MI means each class in the MRO uses ``super()`` to pass control
to the next class, creating a chain.  Without cooperative super() calls,
some classes in the MRO would be skipped.  It matters in diamond hierarchies
and mixin combinations.

**Q3: When should you prefer composition over inheritance?**

Use inheritance for genuine "is-a" relationships where the subclass should
be substitutable for the base class (Liskov Substitution Principle).  Use
composition ("has-a") when you want to reuse implementation without claiming
the substitutability guarantee.  Rule: "favour composition over inheritance".

**Q4: What does** ``isinstance(obj, Base)`` **return for subclass instances?**

``True``.  ``isinstance`` checks the full type hierarchy — it returns ``True``
if ``type(obj)`` is ``Base`` or any subclass of ``Base``.  This is why it is
preferred over ``type(obj) == Base`` for polymorphic code.
