"""Memento Pattern — Example 3: Configuration Rollback.

An application configuration object supports versioned rollback.  Before
applying risky changes, a snapshot is saved; if the new config causes errors,
it is rolled back.
"""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataclasses import dataclass, field
from memento_pattern import Caretaker, Originator


@dataclass
class AppConfig:
    db_host: str = "localhost"
    db_port: int = 5432
    debug: bool = False
    feature_flags: dict[str, bool] = field(default_factory=dict)

    def __repr__(self) -> str:
        flags = self.feature_flags
        return (
            f"Config(db={self.db_host}:{self.db_port}, "
            f"debug={self.debug}, flags={flags})"
        )


def apply_config(config: AppConfig) -> bool:
    """Simulate applying config; fails if debug=True and no flags set."""
    if config.debug and not config.feature_flags:
        print("  [Config] ERROR: debug mode requires feature flags!")
        return False
    print(f"  [Config] Applied: {config}")
    return True


def main() -> None:
    cfg = Originator(AppConfig())
    care = Caretaker(cfg)

    print("=== Baseline config ===")
    apply_config(cfg.state)
    care.save()

    print("\n=== Risky change: enable debug without flags ===")
    s = cfg.state
    cfg.state = AppConfig(s.db_host, s.db_port, True, {})
    if not apply_config(cfg.state):
        print("  Rolling back...")
        care.undo()
        print(f"  Config restored: {cfg.state}")

    print("\n=== Valid change: new DB host ===")
    care.save()
    s = cfg.state
    cfg.state = AppConfig("db.prod.example.com", s.db_port, s.debug, s.feature_flags)
    if apply_config(cfg.state):
        print("  New config accepted.")

    print("\n=== Final config ===")
    print(f"  {cfg.state}")


if __name__ == "__main__":
    main()
