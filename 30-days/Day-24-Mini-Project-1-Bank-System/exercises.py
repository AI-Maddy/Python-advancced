"""
Day 24 — Exercises: Bank System
=================================
Build on the bank system from lesson.py.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Iterator

# Re-use the core classes from lesson.py
from lesson import (
    Account, Bank, CheckingAccount, Customer,
    InsufficientFundsError, NegativeAmountError,
    SavingsAccount, Transaction,
)


# ---------------------------------------------------------------------------
# Exercise 1 — Add LoanAccount
# ---------------------------------------------------------------------------
# TODO: Implement LoanAccount(Account) with:
#   - loan_amount: Decimal (principal)
#   - annual_rate: Decimal
#   - balance starts at -loan_amount (you owe that much)
#   - deposit() = make a payment (reduces debt)
#   - withdraw() raises NotImplementedError
#   - apply_interest() charges monthly interest on the remaining balance
#   - is_paid_off() returns True when balance >= 0

class LoanAccount(Account):
    """TODO: A loan account where balance is negative (you owe money)."""

    account_type = "loan"

    def __init__(
        self,
        account_id: str,
        owner_name: str,
        loan_amount: Decimal,
        annual_rate: Decimal = Decimal("0.08"),
    ) -> None:
        # TODO: initialise — balance should start negative
        ...

    def withdraw(self, amount: Decimal, description: str = "") -> Transaction:
        """TODO: Raise NotImplementedError (cannot borrow more on a loan)."""
        raise NotImplementedError("Cannot withdraw from a loan account")

    def apply_interest(self) -> Transaction | None:
        """TODO: Charge monthly interest on the outstanding balance."""
        ...
        return None

    def is_paid_off(self) -> bool:
        """TODO: Return True when balance >= 0."""
        ...
        return False


def exercise1_loan_account() -> tuple[Decimal, bool, bool]:
    """
    Return (balance_after_payment, interest_applied, paid_off).
    - Open a $1000 loan at 12% annual rate.
    - Apply interest once (should add ~$10).
    - Make a $500 payment.
    - Check if it's paid off (it should not be).
    """
    # TODO
    ...
    return (Decimal("0"), False, False)


# ---------------------------------------------------------------------------
# Exercise 2 — Monthly Statement Generator
# ---------------------------------------------------------------------------
# TODO: Implement generate_monthly_statement(account: Account) -> Iterator[str]
#       as a generator that yields one line at a time:
#         "Account: ACC000001 (savings)"
#         "Balance: $1234.56"
#         "Transactions:"
#         "  2026-04-01 + $100.00 deposit    → $1100.00"
#         "  ..."
#         "---"
# Positive transactions (deposit, transfer_in, interest with +amount) start with '+'.
# Negative transactions start with '-'.

def generate_monthly_statement(account: Account) -> Iterator[str]:
    """TODO: Generate statement lines for an account."""
    # TODO
    ...
    yield ""


def exercise2_statement_generator() -> list[str]:
    """Return list of statement lines for a simple savings account."""
    bank = Bank("Test Bank")
    cust = bank.register_customer("Test User", "test@x.com")
    acc = bank.open_savings(cust, Decimal("1000.00"))
    acc.deposit(Decimal("200.00"), "Bonus")
    acc.withdraw(Decimal("50.00"), "ATM")
    return list(generate_monthly_statement(acc))


# ---------------------------------------------------------------------------
# Exercise 3 — CSV Export with csv module
# ---------------------------------------------------------------------------
# TODO: Implement export_to_csv(account: Account) -> str
#       Returns a CSV string with columns:
#         date, type, amount, balance, description

import csv
import io as _io

def export_to_csv(account: Account) -> str:
    """TODO: Export account transactions as a CSV string."""
    # TODO: use csv.writer
    ...
    return ""


def exercise3_csv_export() -> tuple[int, list[str]]:
    """
    Return (row_count_excluding_header, header_columns) for a 3-transaction account.
    """
    bank = Bank("CSV Bank")
    cust = bank.register_customer("CSV User", "csv@x.com")
    acc = bank.open_savings(cust, Decimal("500.00"))
    acc.deposit(Decimal("100.00"))
    acc.withdraw(Decimal("50.00"))
    csv_str = export_to_csv(acc)
    reader = csv.reader(_io.StringIO(csv_str))
    rows = list(reader)
    header = rows[0] if rows else []
    data_rows = rows[1:]
    return (len(data_rows), header)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_loan_account())
    print("Exercise 2 (first 5 lines):", exercise2_statement_generator()[:5])
    print("Exercise 3:", exercise3_csv_export())
