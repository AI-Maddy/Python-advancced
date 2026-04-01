"""State Pattern — Example 1: Vending Machine.

A vending machine transitions through: Idle → HasMoney → Dispensing → Idle.
Each state handles the relevant actions (insert coin, select item, dispense).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class VendingState(ABC):
    """Abstract vending machine state."""

    @abstractmethod
    def insert_coin(self, machine: VendingMachine, amount: float) -> None: ...

    @abstractmethod
    def select_item(self, machine: VendingMachine, item: str) -> None: ...

    @abstractmethod
    def dispense(self, machine: VendingMachine) -> None: ...

    def __repr__(self) -> str:
        return type(self).__name__


class IdleState(VendingState):
    def insert_coin(self, machine: VendingMachine, amount: float) -> None:
        machine.balance += amount
        print(f"  Coin inserted: ${amount:.2f}. Balance: ${machine.balance:.2f}")
        machine.state = HasMoneyState()

    def select_item(self, machine: VendingMachine, item: str) -> None:
        print("  Please insert a coin first.")

    def dispense(self, machine: VendingMachine) -> None:
        print("  Nothing selected.")


class HasMoneyState(VendingState):
    def insert_coin(self, machine: VendingMachine, amount: float) -> None:
        machine.balance += amount
        print(f"  Additional coin: ${amount:.2f}. Balance: ${machine.balance:.2f}")

    def select_item(self, machine: VendingMachine, item: str) -> None:
        price = machine.inventory.get(item)
        if price is None:
            print(f"  Item '{item}' not found.")
            return
        if machine.balance < price:
            print(f"  Not enough balance (${machine.balance:.2f}) for '{item}' (${price:.2f}).")
            return
        machine.selected = item
        print(f"  Selected: {item} (${price:.2f})")
        machine.state = DispensingState()

    def dispense(self, machine: VendingMachine) -> None:
        print("  Select an item first.")


class DispensingState(VendingState):
    def insert_coin(self, machine: VendingMachine, amount: float) -> None:
        print("  Please wait, dispensing in progress.")

    def select_item(self, machine: VendingMachine, item: str) -> None:
        print("  Already dispensing.")

    def dispense(self, machine: VendingMachine) -> None:
        item = machine.selected
        price = machine.inventory[item]  # type: ignore[index]
        machine.balance -= price
        change = machine.balance
        machine.balance = 0.0
        machine.selected = None
        print(f"  Dispensing {item}. Change: ${change:.2f}")
        machine.state = IdleState()


@dataclass
class VendingMachine:
    inventory: dict[str, float]
    balance: float = 0.0
    selected: str | None = None
    state: VendingState = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.state = IdleState()

    def insert_coin(self, amount: float) -> None:
        self.state.insert_coin(self, amount)

    def select_item(self, item: str) -> None:
        self.state.select_item(self, item)

    def dispense(self) -> None:
        self.state.dispense(self)


def main() -> None:
    vm = VendingMachine(inventory={"Cola": 1.50, "Chips": 1.00, "Water": 0.75})

    print("=== Normal purchase ===")
    vm.insert_coin(1.00)
    vm.insert_coin(0.75)
    vm.select_item("Cola")
    vm.dispense()

    print("\n=== Insufficient funds ===")
    vm.insert_coin(0.50)
    vm.select_item("Cola")

    print("\n=== Invalid item ===")
    vm.select_item("Pizza")


if __name__ == "__main__":
    main()
