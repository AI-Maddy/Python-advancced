# Python Idioms

Pythonic solutions to patterns that C++ solves through language features such as RAII, templates, virtual dispatch, and operator overloading. Each idiom is a standalone module with examples and tests.

## Idioms

| Idiom | C++ Equivalent | File |
|---|---|---|
| Abstract Base Class | Pure virtual class / interface | `abstract-base-class-idiom/abstract_base_class.py` |
| Classmethod Factory | Named constructor idiom | `classmethod-factory-idiom/classmethod_factory.py` |
| Context Manager | RAII (`unique_ptr`, destructors) | `context-manager-idiom/context_manager.py` |
| Dataclass | Rule of Zero / aggregate types | `dataclass-idiom/dataclass_idiom.py` |
| Decorator Function | Higher-order function wrappers | `decorator-function-idiom/decorator_function.py` |
| Descriptor | Operator overloading / member proxies | `descriptor-idiom/descriptor.py` |
| Generator | Coroutine / lazy range | `generator-idiom/generator_idiom.py` |
| Metaclass | Template metaprogramming / type traits | `metaclass-idiom/metaclass.py` |
| Mixin | Multiple inheritance / CRTP | `mixin-idiom/mixin_idiom.py` |
| Protocol | C++ Concepts / type erasure | `protocol-idiom/protocol_idiom.py` |
| Singledispatch | Function overloading / tag dispatch | `singledispatch-idiom/singledispatch_idiom.py` |
| Slots | Struct / fixed-layout class | `slots-idiom/slots_idiom.py` |

## Directory Layout

Each idiom directory contains:

```
<idiom-name>/
    <idiom_name>.py     # Core implementation
    example_1.py        # First usage scenario
    example_2.py        # Second usage scenario
    tests/
        test_<idiom_name>.py
```

## Run

```bash
# All idiom tests
python -m pytest python-idioms/ -q

# A single idiom
python -m pytest python-idioms/context-manager-idiom/ -v
```
