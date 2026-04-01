"""Command Pattern — Example 2: Transaction Queue.

Commands are queued and executed in batch (like a database transaction).
If any command fails, previously executed commands in the batch are rolled back.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...


@dataclass
class BankAccount:
    """Simple bank account receiver."""
    owner: str
    balance: float = 0.0

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError(f"Insufficient funds: need {amount}, have {self.balance}")
        self.balance -= amount

    def __str__(self) -> str:
        return f"{self.owner}: ${self.balance:.2f}"


@dataclass
class DepositCommand(Command):
    account: BankAccount
    amount: float

    def execute(self) -> None:
        self.account.deposit(self.amount)
        print(f"  Deposited ${self.amount:.2f} → {self.account}")

    def undo(self) -> None:
        self.account.withdraw(self.amount)
        print(f"  Rolled back deposit ${self.amount:.2f} → {self.account}")


@dataclass
class WithdrawCommand(Command):
    account: BankAccount
    amount: float

    def execute(self) -> None:
        self.account.withdraw(self.amount)
        print(f"  Withdrew ${self.amount:.2f} → {self.account}")

    def undo(self) -> None:
        self.account.deposit(self.amount)
        print(f"  Rolled back withdrawal ${self.amount:.2f} → {self.account}")


class TransactionQueue:
    """Batches commands and rolls back on failure."""

    def __init__(self) -> None:
        self._queue: list[Command] = []

    def add(self, command: Command) -> None:
        self._queue.append(command)

    def commit(self) -> bool:
        executed: list[Command] = []
        try:
            for cmd in self._queue:
                cmd.execute()
                executed.append(cmd)
            self._queue.clear()
            return True
        except Exception as exc:
            print(f"  Transaction failed: {exc} — rolling back")
            for cmd in reversed(executed):
                cmd.undo()
            self._queue.clear()
            return False


def main() -> None:
    alice = BankAccount("Alice", 1000.0)
    bob = BankAccount("Bob", 500.0)

    print("=== Successful transaction ===")
    txn = TransactionQueue()
    txn.add(WithdrawCommand(alice, 200.0))
    txn.add(DepositCommand(bob, 200.0))
    txn.commit()
    print(f"  Final: {alice}, {bob}\n")

    print("=== Failed transaction (rollback) ===")
    txn2 = TransactionQueue()
    txn2.add(WithdrawCommand(alice, 500.0))
    txn2.add(WithdrawCommand(alice, 400.0))  # this will fail
    txn2.commit()
    print(f"  Final: {alice}, {bob}")


if __name__ == "__main__":
    main()
