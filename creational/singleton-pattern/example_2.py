"""
Example 2 — Application config registry singleton.

Shows that configuration written through one reference is visible through
every other reference obtained independently.
"""
from __future__ import annotations

from singleton import ConfigRegistry


def configure_app() -> None:
    cfg = ConfigRegistry()
    cfg.set("log_level", "DEBUG")
    cfg.set("max_retries", 3)
    cfg.set("timeout_sec", 30)


def read_config_in_another_module() -> None:
    cfg = ConfigRegistry()   # Same instance — no constructor args needed
    print(f"log_level  = {cfg.get('log_level')}")
    print(f"max_retries= {cfg.get('max_retries')}")
    print(f"timeout_sec= {cfg.get('timeout_sec')}")
    print(f"unknown    = {cfg.get('unknown', 'N/A')}")


def main() -> None:
    configure_app()
    read_config_in_another_module()

    c1 = ConfigRegistry()
    c2 = ConfigRegistry()
    print(f"\nSame object? {c1 is c2}")   # True
    print(repr(c1))


if __name__ == "__main__":
    main()
