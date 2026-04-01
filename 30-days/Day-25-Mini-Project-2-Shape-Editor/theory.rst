Day 25 — Mini-Project 2: Shape Editor
=======================================

Design Overview
----------------

The shape editor demonstrates the **Visitor** and **Composite** patterns
together with **Protocol**-based type checking.

Visitor Pattern
---------------

Separates an algorithm (area, perimeter, SVG rendering) from the object
structure (Circle, Rectangle, ...).  Add new operations without modifying
shapes; add new shapes by updating visitors.

.. code-block:: python

    class ShapeVisitor(Protocol):
        def visit_circle(self, s: Circle) -> object: ...
        def visit_rectangle(self, s: Rectangle) -> object: ...
        # ...

    class Circle(Shape):
        def accept(self, visitor: ShapeVisitor) -> object:
            return visitor.visit_circle(self)  # double dispatch

Composite Pattern (ShapeGroup)
--------------------------------

``ShapeGroup`` contains a list of ``Shape`` children and itself satisfies
the ``Shape`` interface.  Visitors recurse transparently.

.. code-block:: python

    group = ShapeGroup(name="scene")
    group.add(Circle(50, 50, 30))
    group.add(Rectangle(0, 0, 100, 60))
    area = AreaCalculator().calculate(group)   # sums children

``__post_init__`` Validation
-----------------------------

Dataclass ``__post_init__`` validates fields after ``__init__`` runs:

.. code-block:: python

    @dataclass
    class Circle(Shape):
        radius: float

        def __post_init__(self) -> None:
            if self.radius <= 0:
                raise ValueError(f"radius must be > 0, got {self.radius}")

Area Formulas
-------------

.. list-table::
   :header-rows: 1

   * - Shape
     - Area
     - Perimeter
   * - Circle
     - π r²
     - 2π r
   * - Rectangle
     - w × h
     - 2(w + h)
   * - Triangle
     - ½ |x₁(y₂-y₃) + x₂(y₃-y₁) + x₃(y₁-y₂)|
     - sum of 3 sides
   * - Polygon
     - Shoelace formula
     - sum of all edges
   * - Ellipse
     - π rx ry
     - Ramanujan approximation

Protocol vs ABC for Visitor
-----------------------------

Using ``Protocol`` for ``ShapeVisitor`` means:

* New visitor classes don't need to inherit from anything.
* They just need to implement all ``visit_*`` methods.
* Works with ``isinstance`` when ``@runtime_checkable`` is added.
