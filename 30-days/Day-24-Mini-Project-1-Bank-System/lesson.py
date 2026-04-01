"""
Day 24 — Mini-Project 1: Bank System
======================================
Classes: Account (ABC), SavingsAccount, CheckingAccount,
         Transaction (frozen dataclass), Customer, Bank

Features:
  - deposit/withdraw with validation
  - transfer between accounts
  - transaction history
  - overdraft protection
  - interest calculation
  - Decimal for money precision
"""
from __future__ import annotations

import csv
import io
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import ClassVar


# ===========================================================================
# Transaction — immutable record of a money movement
# ===========================================================================

@dataclass(frozen=True)
class Transaction:
    """
    Immutable record of a single account operation.

    Attributes:
        id: Unique identifier (UUID4 hex).
        type: 'deposit', 'withdrawal', 'transfer_in', 'transfer_out', 'interest'.
        amount: Absolute value in Decimal.
        balance_after: Account balance immediately after this transaction.
        timestamp: UTC datetime of the transaction.
        description: Optional human-readable note.
    """
    id: str
    type: str
    amount: Decimal
    balance_after: Decimal
    timestamp: datetime
    description: str = ""

    @staticmethod
    def make_id() -> str:
        """Generate a unique transaction ID."""
        return uuid.uuid4().hex[:12]


# ===========================================================================
# Account — abstract base class
# ===========================================================================

class InsufficientFundsError(Exception):
    """Raised when a withdrawal or transfer exceeds available balance."""


class NegativeAmountError(ValueError):
    """Raised when an amount is zero or negative."""


class Account(ABC):
    """
    Abstract bank account.

    Subclasses must implement:
      - account_type (class attribute string)
      - apply_interest() method
    """

    account_type: ClassVar[str] = "generic"

    def __init__(self, account_id: str, owner_name: str, initial_deposit: Decimal) -> None:
        if initial_deposit < Decimal("0"):
            raise NegativeAmountError("Initial deposit cannot be negative")
        self._id = account_id
        self._owner = owner_name
        self._balance: Decimal = Decimal("0")
        self._history: list[Transaction] = []
        if initial_deposit > 0:
            self._record("deposit", initial_deposit, "Account opening deposit")

    # --- Public properties ---

    @property
    def account_id(self) -> str:
        """Unique account identifier."""
        return self._id

    @property
    def owner(self) -> str:
        """Name of the account owner."""
        return self._owner

    @property
    def balance(self) -> Decimal:
        """Current balance."""
        return self._balance

    @property
    def history(self) -> list[Transaction]:
        """Read-only snapshot of transaction history."""
        return list(self._history)

    # --- Money operations ---

    def deposit(self, amount: Decimal, description: str = "") -> Transaction:
        """
        Credit amount to this account.

        Raises:
            NegativeAmountError: if amount <= 0.
        """
        self._validate_positive(amount, "Deposit")
        return self._record("deposit", amount, description)

    def withdraw(self, amount: Decimal, description: str = "") -> Transaction:
        """
        Debit amount from this account.

        Raises:
            NegativeAmountError: if amount <= 0.
            InsufficientFundsError: if balance would go below overdraft limit.
        """
        self._validate_positive(amount, "Withdrawal")
        self._check_funds(amount)
        return self._record("withdrawal", -amount, description)

    def transfer_to(self, target: Account, amount: Decimal) -> tuple[Transaction, Transaction]:
        """
        Transfer amount to target account atomically.

        Returns:
            (debit_txn, credit_txn) tuple.
        """
        self._validate_positive(amount, "Transfer")
        self._check_funds(amount)
        debit  = self._record("transfer_out", -amount, f"Transfer to {target.account_id}")
        credit = target._record("transfer_in", amount, f"Transfer from {self.account_id}")
        return (debit, credit)

    # --- Interest ---

    @abstractmethod
    def apply_interest(self) -> Transaction | None:
        """Apply interest or fee; return resulting Transaction (or None)."""

    # --- Internal helpers ---

    def _record(self, txn_type: str, signed_amount: Decimal, description: str) -> Transaction:
        self._balance = (self._balance + signed_amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        txn = Transaction(
            id=Transaction.make_id(),
            type=txn_type,
            amount=abs(signed_amount),
            balance_after=self._balance,
            timestamp=datetime.utcnow(),
            description=description,
        )
        self._history.append(txn)
        return txn

    def _validate_positive(self, amount: Decimal, label: str) -> None:
        if amount <= 0:
            raise NegativeAmountError(f"{label} amount must be positive, got {amount}")

    def _check_funds(self, amount: Decimal) -> None:
        """Override in subclasses that allow overdraft."""
        if self._balance < amount:
            raise InsufficientFundsError(
                f"Insufficient funds: balance={self._balance}, requested={amount}"
            )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(id={self._id!r}, owner={self._owner!r}, "
            f"balance={self._balance})"
        )


# ===========================================================================
# SavingsAccount
# ===========================================================================

class SavingsAccount(Account):
    """
    Savings account with configurable annual interest rate.

    Interest is calculated as balance * (annual_rate / 12) per call to
    apply_interest() (monthly compounding assumption).
    """

    account_type: ClassVar[str] = "savings"

    def __init__(
        self,
        account_id: str,
        owner_name: str,
        initial_deposit: Decimal,
        annual_rate: Decimal = Decimal("0.05"),
    ) -> None:
        super().__init__(account_id, owner_name, initial_deposit)
        self.annual_rate = annual_rate

    def apply_interest(self) -> Transaction | None:
        """Credit monthly interest to the account."""
        if self._balance <= 0:
            return None
        monthly_rate = self.annual_rate / Decimal("12")
        interest = (self._balance * monthly_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return self._record("interest", interest, "Monthly interest")


# ===========================================================================
# CheckingAccount
# ===========================================================================

class CheckingAccount(Account):
    """
    Checking account with optional overdraft protection.

    Overdraft allows balance to go negative up to overdraft_limit.
    A monthly fee is deducted via apply_interest().
    """

    account_type: ClassVar[str] = "checking"

    def __init__(
        self,
        account_id: str,
        owner_name: str,
        initial_deposit: Decimal,
        overdraft_limit: Decimal = Decimal("0"),
        monthly_fee: Decimal = Decimal("5.00"),
    ) -> None:
        super().__init__(account_id, owner_name, initial_deposit)
        self.overdraft_limit = overdraft_limit
        self.monthly_fee = monthly_fee

    def _check_funds(self, amount: Decimal) -> None:
        """Allow withdrawal down to -overdraft_limit."""
        available = self._balance + self.overdraft_limit
        if amount > available:
            raise InsufficientFundsError(
                f"Exceeds overdraft limit: balance={self._balance}, "
                f"limit={self.overdraft_limit}, requested={amount}"
            )

    def apply_interest(self) -> Transaction | None:
        """Deduct monthly fee."""
        if self.monthly_fee > 0:
            return self._record("interest", -self.monthly_fee, "Monthly fee")
        return None


# ===========================================================================
# Customer
# ===========================================================================

class Customer:
    """
    A bank customer who can own multiple accounts.
    """

    def __init__(self, customer_id: str, name: str, email: str) -> None:
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self._accounts: dict[str, Account] = {}

    def add_account(self, account: Account) -> None:
        """Attach an account to this customer."""
        self._accounts[account.account_id] = account

    def get_account(self, account_id: str) -> Account:
        """Retrieve an account by ID."""
        try:
            return self._accounts[account_id]
        except KeyError:
            raise KeyError(f"Account {account_id!r} not found for customer {self.name!r}") from None

    @property
    def accounts(self) -> list[Account]:
        """All accounts belonging to this customer."""
        return list(self._accounts.values())

    def net_worth(self) -> Decimal:
        """Sum of all account balances."""
        return sum((a.balance for a in self._accounts.values()), Decimal("0"))

    def monthly_statement(self) -> str:
        """Generate a text statement for all accounts."""
        lines = [f"=== Statement for {self.name} ==="]
        for acc in self._accounts.values():
            lines.append(f"\n{acc.account_type.title()} {acc.account_id}: ${acc.balance:.2f}")
            for txn in acc.history[-5:]:   # last 5 transactions
                sign = "+" if txn.type in ("deposit", "transfer_in", "interest") and txn.amount > 0 else "-"
                lines.append(
                    f"  {txn.timestamp.strftime('%Y-%m-%d %H:%M')} "
                    f"{sign}${txn.amount:.2f} ({txn.type}) → ${txn.balance_after:.2f}"
                )
        lines.append(f"\nNet worth: ${self.net_worth():.2f}")
        return "\n".join(lines)


# ===========================================================================
# Bank
# ===========================================================================

class Bank:
    """
    Top-level bank that manages customers and accounts.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self._customers: dict[str, Customer] = {}
        self._accounts: dict[str, Account] = {}
        self._account_counter: int = 0

    def _next_account_id(self) -> str:
        self._account_counter += 1
        return f"ACC{self._account_counter:06d}"

    def register_customer(self, name: str, email: str) -> Customer:
        """Create and register a new customer."""
        cid = f"CUST{len(self._customers) + 1:04d}"
        customer = Customer(cid, name, email)
        self._customers[cid] = customer
        return customer

    def open_savings(
        self,
        customer: Customer,
        initial_deposit: Decimal,
        annual_rate: Decimal = Decimal("0.05"),
    ) -> SavingsAccount:
        """Open a savings account for a customer."""
        acc = SavingsAccount(
            self._next_account_id(), customer.name, initial_deposit, annual_rate
        )
        customer.add_account(acc)
        self._accounts[acc.account_id] = acc
        return acc

    def open_checking(
        self,
        customer: Customer,
        initial_deposit: Decimal,
        overdraft_limit: Decimal = Decimal("0"),
    ) -> CheckingAccount:
        """Open a checking account for a customer."""
        acc = CheckingAccount(
            self._next_account_id(), customer.name, initial_deposit, overdraft_limit
        )
        customer.add_account(acc)
        self._accounts[acc.account_id] = acc
        return acc

    def apply_all_interest(self) -> None:
        """Apply interest/fees to all accounts."""
        for acc in self._accounts.values():
            acc.apply_interest()

    def export_transactions_csv(self, account: Account) -> str:
        """Return CSV string of all transactions for an account."""
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["id", "type", "amount", "balance_after", "timestamp", "description"])
        for txn in account.history:
            writer.writerow([
                txn.id,
                txn.type,
                str(txn.amount),
                str(txn.balance_after),
                txn.timestamp.isoformat(),
                txn.description,
            ])
        return buf.getvalue()

    def total_assets(self) -> Decimal:
        """Sum of all account balances."""
        return sum((a.balance for a in self._accounts.values()), Decimal("0"))


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 24 — Bank System")
    print("=" * 60)

    bank = Bank("Python National Bank")

    # Register customers
    alice = bank.register_customer("Alice", "alice@example.com")
    bob   = bank.register_customer("Bob",   "bob@example.com")

    # Open accounts
    alice_savings  = bank.open_savings(alice, Decimal("1000.00"), annual_rate=Decimal("0.06"))
    alice_checking = bank.open_checking(alice, Decimal("500.00"), overdraft_limit=Decimal("200.00"))
    bob_savings    = bank.open_savings(bob, Decimal("2000.00"))

    # Transactions
    alice_savings.deposit(Decimal("250.00"), "Paycheck")
    alice_checking.withdraw(Decimal("100.00"), "Groceries")
    alice_savings.transfer_to(bob_savings, Decimal("300.00"))

    # Overdraft demo
    try:
        alice_checking.withdraw(Decimal("800.00"), "Big purchase")
    except InsufficientFundsError as e:
        print(f"\nOverdraft blocked: {e}")

    # Interest
    bank.apply_all_interest()

    # Statements
    print("\n" + alice.monthly_statement())
    print("\n" + bob.monthly_statement())

    # CSV export
    csv_data = bank.export_transactions_csv(alice_savings)
    print("\nCSV export (first 3 lines):")
    for line in csv_data.splitlines()[:3]:
        print(" ", line)

    print(f"\nBank total assets: ${bank.total_assets():.2f}")
