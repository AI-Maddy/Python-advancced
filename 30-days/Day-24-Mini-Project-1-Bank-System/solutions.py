"""
Day 24 — Solutions: Bank System
=================================
"""
from __future__ import annotations

import csv
import io
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterator

from lesson import (
    Account, Bank, CheckingAccount, Customer,
    InsufficientFundsError, NegativeAmountError,
    SavingsAccount, Transaction,
)


# ---------------------------------------------------------------------------
# Solution 1 — LoanAccount
# ---------------------------------------------------------------------------

class LoanAccount(Account):
    """Loan account: balance starts negative; deposits reduce debt."""

    account_type = "loan"

    def __init__(
        self,
        account_id: str,
        owner_name: str,
        loan_amount: Decimal,
        annual_rate: Decimal = Decimal("0.08"),
    ) -> None:
        # Don't call super().__init__ with initial_deposit to avoid opening record
        # Use object.__init__ approach: set up fields manually
        self._id = account_id
        self._owner = owner_name
        self._balance: Decimal = -loan_amount.quantize(Decimal("0.01"))
        self._history: list[Transaction] = []
        self.annual_rate = annual_rate
        self.loan_amount = loan_amount
        # Record the loan disbursement
        self._record("deposit", -loan_amount, f"Loan of ${loan_amount}")

    def withdraw(self, amount: Decimal, description: str = "") -> Transaction:
        """Cannot borrow more on an existing loan."""
        raise NotImplementedError("Cannot withdraw from a loan account")

    def _check_funds(self, amount: Decimal) -> None:
        """Loan accounts don't need a fund check for payments (deposits)."""

    def apply_interest(self) -> Transaction | None:
        """Charge monthly interest on outstanding balance (negative)."""
        if self._balance >= 0:
            return None  # paid off
        monthly_rate = self.annual_rate / Decimal("12")
        interest = (abs(self._balance) * monthly_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        # Interest increases the debt (makes balance more negative)
        return self._record("interest", -interest, "Monthly interest charge")

    def is_paid_off(self) -> bool:
        """Return True when debt is cleared."""
        return self._balance >= 0


def exercise1_loan_account() -> tuple[Decimal, bool, bool]:
    """Open $1000 loan at 12%, apply interest, make $500 payment."""
    acc = LoanAccount("LOAN001", "Borrower", Decimal("1000.00"), Decimal("0.12"))
    interest_txn = acc.apply_interest()        # charges ~$10
    acc.deposit(Decimal("500.00"), "Payment")  # reduces debt
    return (acc.balance, interest_txn is not None, acc.is_paid_off())


# ---------------------------------------------------------------------------
# Solution 2 — Monthly Statement Generator
# ---------------------------------------------------------------------------

def generate_monthly_statement(account: Account) -> Iterator[str]:
    """Generate statement lines one by one."""
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
    bank = Bank("Test Bank")
    cust = bank.register_customer("Test User", "test@x.com")
    acc = bank.open_savings(cust, Decimal("1000.00"))
    acc.deposit(Decimal("200.00"), "Bonus")
    acc.withdraw(Decimal("50.00"), "ATM")
    return list(generate_monthly_statement(acc))


# ---------------------------------------------------------------------------
# Solution 3 — CSV Export
# ---------------------------------------------------------------------------

def export_to_csv(account: Account) -> str:
    """Export account transactions as a CSV string."""
    buf = io.StringIO()
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
    bank = Bank("CSV Bank")
    cust = bank.register_customer("CSV User", "csv@x.com")
    acc = bank.open_savings(cust, Decimal("500.00"))
    acc.deposit(Decimal("100.00"))
    acc.withdraw(Decimal("50.00"))
    csv_str = export_to_csv(acc)
    reader = csv.reader(io.StringIO(csv_str))
    rows = list(reader)
    header = rows[0] if rows else []
    data_rows = rows[1:]
    return (len(data_rows), header)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Solution 1:", exercise1_loan_account())
    print("Solution 2 (first 5 lines):", exercise2_statement_generator()[:5])
    print("Solution 3:", exercise3_csv_export())
