"""Template Method Pattern — Example 2: Game AI Turn.

Different game AI opponents (aggressive, defensive, random) share the
same turn structure: perceive → decide → act — but implement each step
differently.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random


@dataclass
class GameState:
    player_hp: int = 100
    enemy_hp: int = 100
    turn: int = 0


class GameAI(ABC):
    """Abstract AI — template method is ``take_turn()``."""

    def take_turn(self, state: GameState) -> str:
        """Template: perceive → decide → act."""
        state.turn += 1
        perception = self.perceive(state)
        decision = self.decide(perception, state)
        result = self.act(decision, state)
        return result

    @abstractmethod
    def perceive(self, state: GameState) -> dict[str, object]:
        """Observe the game state and return a perception dict."""

    @abstractmethod
    def decide(self, perception: dict[str, object], state: GameState) -> str:
        """Choose an action based on perception."""

    @abstractmethod
    def act(self, decision: str, state: GameState) -> str:
        """Execute the chosen action and update state."""


class AggressiveAI(GameAI):
    """Always attacks."""

    def perceive(self, state: GameState) -> dict[str, object]:
        return {"player_hp": state.player_hp, "threat": "high"}

    def decide(self, perception: dict[str, object], state: GameState) -> str:
        return "attack"

    def act(self, decision: str, state: GameState) -> str:
        dmg = random.randint(15, 25)
        state.player_hp = max(0, state.player_hp - dmg)
        return f"[AggressiveAI] Turn {state.turn}: ATTACK for {dmg} dmg. Player HP: {state.player_hp}"


class DefensiveAI(GameAI):
    """Heals if low HP, otherwise attacks."""

    def perceive(self, state: GameState) -> dict[str, object]:
        return {"own_hp": state.enemy_hp, "player_hp": state.player_hp}

    def decide(self, perception: dict[str, object], state: GameState) -> str:
        return "heal" if state.enemy_hp < 40 else "attack"

    def act(self, decision: str, state: GameState) -> str:
        if decision == "heal":
            heal = random.randint(10, 20)
            state.enemy_hp = min(100, state.enemy_hp + heal)
            return f"[DefensiveAI] Turn {state.turn}: HEAL +{heal}. Enemy HP: {state.enemy_hp}"
        dmg = random.randint(5, 15)
        state.player_hp = max(0, state.player_hp - dmg)
        return f"[DefensiveAI] Turn {state.turn}: ATTACK for {dmg} dmg. Player HP: {state.player_hp}"


class RandomAI(GameAI):
    """Randomly picks attack, heal, or skip."""
    ACTIONS = ["attack", "heal", "skip"]

    def perceive(self, state: GameState) -> dict[str, object]:
        return {}

    def decide(self, perception: dict[str, object], state: GameState) -> str:
        return random.choice(self.ACTIONS)

    def act(self, decision: str, state: GameState) -> str:
        if decision == "attack":
            dmg = random.randint(1, 30)
            state.player_hp = max(0, state.player_hp - dmg)
            return f"[RandomAI] Turn {state.turn}: ATTACK for {dmg} dmg"
        if decision == "heal":
            heal = random.randint(1, 15)
            state.enemy_hp = min(100, state.enemy_hp + heal)
            return f"[RandomAI] Turn {state.turn}: HEAL +{heal}"
        return f"[RandomAI] Turn {state.turn}: SKIP"


def simulate(ai: GameAI, turns: int = 5) -> None:
    state = GameState()
    for _ in range(turns):
        print(" ", ai.take_turn(state))


def main() -> None:
    random.seed(7)
    print("=== Aggressive AI ===")
    simulate(AggressiveAI())
    print("\n=== Defensive AI (starts low HP) ===")
    state = GameState(enemy_hp=30)
    ai = DefensiveAI()
    for _ in range(5):
        print(" ", ai.take_turn(state))
    print("\n=== Random AI ===")
    simulate(RandomAI())


if __name__ == "__main__":
    main()
