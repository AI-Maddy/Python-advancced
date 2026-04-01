==========================================
Interpreter Pattern — Python Guide
==========================================

Overview
--------
The Interpreter pattern defines a representation for a language's grammar
along with an interpreter that uses that representation to interpret sentences
in the language.

Intent
------
Build a grammar tree for simple languages and evaluate it recursively.

Structure
---------
.. code-block:: text

    Client ──► Context (dict)
    Client ──► Expression (ABC)
                    │
        ┌───────────┼────────────┐
    NumberExpr  AddExpr     MultiplyExpr
    VariableExpr  SubtractExpr  DivideExpr
                    │
               interpret(context) → value

Participants
------------
- **Expression (ABC)** — abstract ``interpret(context)`` interface.
- **TerminalExpression** — interprets a terminal symbol (number, variable).
- **NonTerminalExpression** — composite expression; holds child expressions
  and combines their results.
- **Context** — global state shared by all expressions (variable bindings).
- **Client** — builds the expression tree (or uses a parser to do so).

Python-specific Notes
---------------------
- ``@dataclass(frozen=True)`` creates immutable expression nodes, which is
  safe for recursive evaluation.
- A recursive-descent parser (as shown) is idiomatic Python for small
  grammars.  For larger grammars consider ``lark``, ``pyparsing``, or PLY.
- Generator expressions and comprehensions can replace many Interpreter
  usages for simple transformations.
- Python's ``ast`` module provides a full AST interpreter for Python itself
  — a production-grade example of this pattern.

When to Use
-----------
- The grammar is simple and performance is not critical.
- Efficiency is not a concern (complex grammars → use a parser generator).
- The language sentences need to be interpreted rather than compiled.

Pitfalls
--------
- Class explosion for complex grammars — each rule needs a class.
- Interpreter pattern is inefficient for deeply nested expressions (stack
  depth, repeated evaluation).
- Prefer a dedicated parsing library for non-trivial grammars.

Related Patterns
----------------
- **Composite** — the expression tree is a Composite.
- **Visitor** — can be used to evaluate or print the expression tree.
- **Iterator** — to walk the expression tree.
