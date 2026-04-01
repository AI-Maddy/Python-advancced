# Proxy Pattern

Provides a surrogate or placeholder for another object to control access to it. Three variants: virtual proxy (lazy initialisation), protection proxy (access control), and caching proxy (memoisation).

## C++ Equivalent
Class implementing the same interface as the real subject; holds a pointer/reference to the real object and intercepts calls.

## Files

| File | Description |
|---|---|
| `proxy.py` | Core implementation: `Service` ABC, `RealService`, `VirtualProxy`, `ProtectionProxy`, `CachingProxy` |
| `example_1.py` | Virtual proxy — lazy-loaded high-resolution image |
| `example_2.py` | Protection proxy — role-based access to a document |
| `tests/test_proxy.py` | pytest suite |

## Run

```bash
python proxy.py                     # demo
python -m pytest tests/ -v          # tests
```

## Key Classes

- `Service` — ABC with `request(query)` method
- `RealService` — the actual (heavyweight) service
- `VirtualProxy` — creates `RealService` only on first access
- `ProtectionProxy` — checks caller role before delegating
- `CachingProxy` — caches results of expensive requests
