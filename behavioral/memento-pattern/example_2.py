"""Memento Pattern — Example 2: Game Save State.

A player's position, health, and inventory are snapshotted before entering
a boss fight.  If the player dies, the save is restored.
"""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataclasses import dataclass, field
from memento_pattern import Caretaker, Originator


@dataclass
class PlayerState:
    x: float
    y: float
    health: int
    inventory: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return (
            f"Player(pos=({self.x},{self.y}), hp={self.health}, "
            f"inv={self.inventory})"
        )


def main() -> None:
    player = Originator(PlayerState(0.0, 0.0, 100, ["sword", "shield"]))
    care = Caretaker(player)

    def show(label: str) -> None:
        print(f"  [{label}] {player.state}")

    show("Start")
    care.save()   # checkpoint before dungeon

    # Explore dungeon
    s = player.state
    player.state = PlayerState(s.x + 10, s.y + 5, s.health - 20, s.inventory + ["potion"])
    show("In dungeon")
    care.save()  # mid-dungeon save

    # Enter boss room — big risk, save first
    s = player.state
    player.state = PlayerState(s.x + 3, s.y + 1, s.health, s.inventory)
    show("Boss room entry")
    care.save()

    # Player dies in boss fight
    s = player.state
    player.state = PlayerState(s.x, s.y, 0, s.inventory)
    show("After death")

    print("\n--- Restore last save ---")
    care.undo()
    show("Restored")

    print("\n--- Restore to dungeon entry ---")
    care.undo()
    show("Restored to dungeon")


if __name__ == "__main__":
    main()
