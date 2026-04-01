Day 24 — Mini-Project 1: Bank System
======================================

Design Decisions
-----------------

**Decimal for money**
    Python's ``float`` has binary rounding errors (0.1 + 0.2 ≠ 0.3).
    Always use ``decimal.Decimal`` for financial calculations.

.. code-block:: python

    from decimal import Decimal, ROUND_HALF_UP
    amount = Decimal("19.99")
    tax = (amount * Decimal("0.08")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

**frozen dataclass for Transaction**
    Transactions are immutable facts — once recorded, they cannot change.
    ``@dataclass(frozen=True)`` enforces this at the Python level.

**ABC for Account**
    ``SavingsAccount`` and ``CheckingAccount`` share a common interface.
    The abstract ``apply_interest()`` forces subclasses to implement it.

**Overdraft as policy in subclass**
    ``_check_funds()`` is a template method overridden in ``CheckingAccount``,
    avoiding ``isinstance`` checks in the base class (Open/Closed Principle).

**Customer owns accounts; Bank owns customers**
    A clear ownership hierarchy prevents circular references and simplifies
    serialisation.

Class Diagram
-------------

.. code-block:: text

    Bank
    ├── Customer (1..*)
    │   └── Account (1..*)
    │       ├── SavingsAccount
    │       ├── CheckingAccount
    │       └── LoanAccount (exercise)
    └── Transaction (1..*) via Account.history

Key Patterns Used
------------------

* **Template Method** — ``withdraw()`` calls ``_check_funds()`` which subclasses override.
* **Value Object** — ``Transaction`` is a frozen dataclass (no identity, only value).
* **Factory Methods** — ``Bank.open_savings()``, ``Bank.open_checking()``.
* **Decimal Precision** — all arithmetic quantized to 2 decimal places.

Testing Tips
------------

* Use ``pytest.raises(InsufficientFundsError)`` for overdraft tests.
* Use ``Decimal("0.01")`` precision in assertions:
  ``assert acc.balance == pytest.approx(Decimal("100.00"), abs=Decimal("0.01"))``
* Parametrize deposit/withdraw amounts including edge cases: 0, negative, very large.
