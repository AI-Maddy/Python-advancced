"""
Example 2 — Bank account facade.

Hides balance checker, fraud detector, and transaction logger behind a
simple transfer() interface.
"""
from __future__ import annotations


class BalanceChecker:
    def __init__(self) -> None:
        self._balances: dict[str, float] = {"ACC001": 1000.0, "ACC002": 500.0}

    def get_balance(self, account: str) -> float:
        return self._balances.get(account, 0.0)

    def debit(self, account: str, amount: float) -> bool:
        if self._balances.get(account, 0.0) >= amount:
            self._balances[account] -= amount
            return True
        return False

    def credit(self, account: str, amount: float) -> None:
        self._balances[account] = self._balances.get(account, 0.0) + amount


class FraudDetector:
    def check(self, account: str, amount: float) -> bool:
        if amount > 10_000:
            print(f"  FraudDetector: flagged large transfer {amount:.2f} from {account}")
            return False
        return True


class TransactionLogger:
    def __init__(self) -> None:
        self._log: list[str] = []

    def record(self, from_acc: str, to_acc: str, amount: float, status: str) -> None:
        entry = f"TRANSFER {from_acc}→{to_acc} ${amount:.2f} [{status}]"
        self._log.append(entry)
        print(f"  Logger: {entry}")

    @property
    def entries(self) -> list[str]:
        return list(self._log)


class BankFacade:
    """Simple transfer(from, to, amount) → bool facade."""

    def __init__(self) -> None:
        self._checker = BalanceChecker()
        self._fraud = FraudDetector()
        self._logger = TransactionLogger()

    def transfer(self, from_acc: str, to_acc: str, amount: float) -> bool:
        if not self._fraud.check(from_acc, amount):
            self._logger.record(from_acc, to_acc, amount, "BLOCKED")
            return False
        if not self._checker.debit(from_acc, amount):
            self._logger.record(from_acc, to_acc, amount, "INSUFFICIENT_FUNDS")
            return False
        self._checker.credit(to_acc, amount)
        self._logger.record(from_acc, to_acc, amount, "OK")
        return True

    def balance(self, account: str) -> float:
        return self._checker.get_balance(account)


def main() -> None:
    bank = BankFacade()
    print(f"ACC001 balance: ${bank.balance('ACC001'):.2f}")
    bank.transfer("ACC001", "ACC002", 200.0)
    print(f"ACC001 balance after transfer: ${bank.balance('ACC001'):.2f}")
    bank.transfer("ACC001", "ACC002", 50_000.0)  # should be blocked
    bank.transfer("ACC001", "ACC002", 10_000.0)  # insufficient funds


if __name__ == "__main__":
    main()
