# Interpreter Pattern

Defines a representation for a language's grammar along with an interpreter that uses that representation to interpret sentences in the language.

## C++ Equivalent
Abstract `Expression` with virtual `interpret(Context&)`; composite expressions recursively evaluate children.

## Files

| File | Description |
|---|---|
| `interpreter_pattern.py` | Core implementation: `Expression` ABC, terminal and composite arithmetic expressions |
| `example_1.py` | Arithmetic expression evaluator with variables |
| `example_2.py` | Boolean logic expression interpreter |
| `example_3.py` | Simple query language interpreter |
| `tests/test_interpreter_pattern.py` | pytest suite |

## Run

```bash
python interpreter_pattern.py       # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Expression` — ABC with `interpret(context: dict)` returning a numeric result
- `NumberExpression`, `VariableExpression` — terminal expressions
- `AddExpression`, `SubtractExpression`, `MultiplyExpression` — composite expressions
- `Context` — type alias for `dict[str, Any]` mapping variable names to values
