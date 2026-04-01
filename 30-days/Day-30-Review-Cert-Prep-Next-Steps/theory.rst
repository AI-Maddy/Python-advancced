Day 30 — Review, Cert-Prep & Next Steps
=========================================

Course Summary
--------------

.. list-table::
   :header-rows: 1
   :widths: 5 20 30

   * - Day
     - Topic
     - Key Takeaways
   * - 16
     - Modules & Packages
     - ``__all__``, ``importlib``, relative imports, sys.path
   * - 17
     - Design Patterns
     - Strategy (callable), Observer (list), Borg, Registry
   * - 18
     - SOLID Principles
     - SRP, OCP, LSP, ISP, DIP applied in Python
   * - 19
     - Testing & TDD
     - pytest fixtures, parametrize, mock, hypothesis
   * - 20
     - Metaclasses
     - type(), SingletonMeta, RegistryMeta, __init_subclass__
   * - 21
     - functools/itertools
     - reduce, partial, lru_cache, groupby, compose()
   * - 22
     - Performance
     - __slots__, cProfile, tracemalloc, timeit
   * - 23
     - Async
     - asyncio, gather, Queue, Lock, Semaphore
   * - 24
     - Bank System
     - ABC, Decimal, frozen dataclass, CSV export
   * - 25
     - Shape Editor
     - Visitor pattern, Composite, Protocol-based dispatch
   * - 26
     - Game ECS
     - Entity-Component-System, EventBus, State Machine
   * - 27
     - Refactoring
     - Extract Method/Class, Polymorphism, DI
   * - 28
     - Code Review
     - Mutable defaults, closures, is vs ==, super()
   * - 29
     - Advanced Topics
     - weakref, pickle, enum, ChainMap, copy, pathlib
   * - 30
     - Review
     - Cheat-sheet, Q&A, next steps

Design Principle Summary
-------------------------

.. list-table::
   :header-rows: 1

   * - Principle
     - One Line
   * - DRY
     - Don't Repeat Yourself
   * - YAGNI
     - You Aren't Gonna Need It
   * - KISS
     - Keep It Simple, Stupid
   * - SRP
     - One reason to change per class
   * - OCP
     - Open for extension, closed for modification
   * - LSP
     - Subtypes must be substitutable
   * - ISP
     - Prefer narrow interfaces / Protocols
   * - DIP
     - Depend on abstractions, inject dependencies
   * - Law of Demeter
     - Only talk to immediate friends

Pythonic Code Checklist
------------------------

- [ ] ``from __future__ import annotations`` on every file
- [ ] Full type hints on every public function and method
- [ ] Docstrings on every class and public method
- [ ] ``__all__`` defined in every public module
- [ ] No mutable default arguments
- [ ] ``super().__init__(**kwargs)`` in multi-inheritance
- [ ] Prefer Protocols over ABCs for interfaces
- [ ] Use ``Decimal`` for money, never ``float``
- [ ] Context managers for resource management
- [ ] Test every public function with pytest
- [ ] Run mypy --strict on CI
- [ ] Run ruff / flake8 for linting

Certification Topics (if pursuing Python Institute / PCep/PCap)
-----------------------------------------------------------------

* Data types and type coercion
* Comprehensions (list, dict, set, generator)
* Exception handling (hierarchy, custom exceptions)
* OOP: class, inheritance, encapsulation, polymorphism
* Modules and packages
* File I/O
* Iterators, generators
* Decorators
* Lambda, map, filter, zip
* Standard library: os, sys, datetime, json, re, collections

Recommended Next Projects
--------------------------

1. Build a REST API with FastAPI + pydantic + SQLAlchemy ORM
2. Implement a command-line tool with click or typer
3. Write a library with full type annotations and hypothesis tests
4. Build a data pipeline with asyncio producers/consumers
5. Contribute to an open-source Python project
