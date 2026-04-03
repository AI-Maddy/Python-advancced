"""
Day 24 — Exercises: Bank System
=================================
Build on the bank system from lesson.py.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
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
        self._id = account_id
        self._owner = owner_name
        self._balance: Decimal = -loan_amount.quantize(Decimal("0.01"))
        self._history: list[Transaction] = []
        self.annual_rate = annual_rate
        self.loan_amount = loan_amount
        # Record the loan disbursement
        self._record("deposit", -loan_amount, f"Loan of ${loan_amount}")

    def _check_funds(self, amount: Decimal) -> None:
        """Loan accounts don't need a fund check for payments (deposits)."""

    def withdraw(self, amount: Decimal, description: str = "") -> Transaction:
        """TODO: Raise NotImplementedError (cannot borrow more on a loan)."""
        raise NotImplementedError("Cannot withdraw from a loan account")

    def apply_interest(self) -> Transaction | None:
        """TODO: Charge monthly interest on the outstanding balance."""
        if self._balance >= 0:
            return None  # paid off
        monthly_rate = self.annual_rate / Decimal("12")
        interest = (abs(self._balance) * monthly_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        # Interest increases the debt (makes balance more negative)
        return self._record("interest", -interest, "Monthly interest charge")

    def is_paid_off(self) -> bool:
        """TODO: Return True when balance >= 0."""
        return self._balance >= 0


def exercise1_loan_account() -> tuple[Decimal, bool, bool]:
    """
    Return (balance_after_payment, interest_applied, paid_off).
    - Open a $1000 loan at 12% annual rate.
    - Apply interest once (should add ~$10).
    - Make a $500 payment.
    - Check if it's paid off (it should not be).
    """
    acc = LoanAccount("LOAN001", "Borrower", Decimal("1000.00"), Decimal("0.12"))
    interest_txn = acc.apply_interest()        # charges ~$10
    acc.deposit(Decimal("500.00"), "Payment")  # reduces debt
    return (acc.balance, interest_txn is not None, acc.is_paid_off())


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
    yield f"Account: {account.account_id} ({account.account_type})"
    yield f"Balance: ${account.balance:.2f}"
    yield "Transactions:"
    for txn in account.history:
        positive_types = {"deposit", "transfer_in"}
        if txn.type in positive_types or (txn.type == "interest" and txn.amount > 0):
            sign = "+"
        else:
            sign = "-"
        date_str = txn.timestamp.strftime("%Y-%m-%d %H:%M")
        label = txn.type.ljust(14)
        yield f"  {date_str} {sign}${txn.amount:.2f} {label} → ${txn.balance_after:.2f}"
    yield "---"


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
    buf = _io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["date", "type", "amount", "balance", "description"])
    for txn in account.history:
        writer.writerow([
            txn.timestamp.strftime("%Y-%m-%d"),
            txn.type,
            str(txn.amount),
            str(txn.balance_after),
            txn.description,
        ])
    return buf.getvalue()


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
