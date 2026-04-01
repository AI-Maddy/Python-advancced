"""
Example 2 — @contextmanager for mocking and temporary state.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from context_manager import temporary_attribute


class Config:
    debug: bool = False
    log_level: str = "INFO"


def process(cfg: Config) -> str:
    return f"debug={cfg.debug} level={cfg.log_level}"


@contextmanager
def debug_mode(cfg: Config) -> Generator[Config, None, None]:
    """Temporarily enable debug mode."""
    old_debug = cfg.debug
    old_level = cfg.log_level
    cfg.debug = True
    cfg.log_level = "DEBUG"
    try:
        yield cfg
    finally:
        cfg.debug = old_debug
        cfg.log_level = old_level


def main() -> None:
    cfg = Config()
    print("Normal:", process(cfg))

    with debug_mode(cfg) as c:
        print("In debug_mode:", process(c))

    print("After debug_mode:", process(cfg))

    # temporary_attribute from context_manager module
    class Obj:
        value = 10

    obj = Obj()
    with temporary_attribute(obj, "value", 99):
        print(f"Inside: obj.value = {obj.value}")
    print(f"Outside: obj.value = {obj.value}")


if __name__ == "__main__":
    main()
