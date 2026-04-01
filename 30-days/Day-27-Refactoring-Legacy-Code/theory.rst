Day 27 — Refactoring Legacy Code
==================================

What is Refactoring?
--------------------

Changing code structure **without changing observable behaviour**.
Tests must pass before and after each refactoring step.

Common Refactoring Techniques
------------------------------

**Extract Method**
    Move a block of code into a named function/method.

.. code-block:: python

    # Before
    total = 0
    for item in items:
        total += item["price"] * item["qty"]

    # After
    def compute_subtotal(items: list[dict]) -> float:
        return sum(i["price"] * i["qty"] for i in items)

**Extract Class**
    Move related fields/methods from a God class into a focused class.

**Replace Conditional with Polymorphism**
    Replace ``if customer_type == "vip": ... elif customer_type == "member": ...``
    with separate Strategy classes.

**Introduce Parameter Object**
    Bundle related arguments into a dataclass.

**Dependency Injection**
    Remove ``self.mailer = SmtpMailer()`` from ``__init__``; accept
    ``mailer: MailerProtocol`` as a parameter instead.

**Type Hints First**
    Adding type hints often reveals hidden coupling and design issues.

Refactoring Process
--------------------

1. Ensure tests exist (write characterisation tests if none exist).
2. Run tests — they must pass.
3. Make one small refactoring change.
4. Run tests again — still passing.
5. Commit.
6. Repeat.

**Never refactor and add features simultaneously.**

Identifying Code Smells
------------------------

.. list-table::
   :header-rows: 1

   * - Smell
     - Fix
   * - Long function (> 20 lines)
     - Extract Method
   * - God class (> 5 responsibilities)
     - Extract Class
   * - Long parameter list (> 4 params)
     - Introduce Parameter Object
   * - Conditional dispatch on type
     - Polymorphism / Strategy
   * - Hard-coded I/O in business logic
     - Dependency Injection
   * - Mutable default argument
     - See Day 28
   * - Global state
     - Extract to class / inject

After Refactoring
-----------------

* Code is easier to read and understand.
* Adding a new discount type doesn't require editing ``OrderProcessor``.
* ``PriceCalculator``, ``InventoryChecker`` are testable in isolation.
* ``NotificationService`` can be swapped for a mock in tests.
