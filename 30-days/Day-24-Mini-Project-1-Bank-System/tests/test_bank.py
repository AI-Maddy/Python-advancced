"""
Tests for Day 24 — Bank System
Run with: pytest tests/test_bank.py -v
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

import pytest

# Allow importing from parent dir
sys.path.insert(0, str(Path(__file__).parent.parent))

from lesson import (
    Account, Bank, CheckingAccount, Customer,
    InsufficientFundsError, NegativeAmountError,
    SavingsAccount, Transaction,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def bank() -> Bank:
    return Bank("Test Bank")


@pytest.fixture
def alice(bank: Bank) -> Customer:
    return bank.register_customer("Alice", "alice@test.com")


@pytest.fixture
def savings(bank: Bank, alice: Customer) -> SavingsAccount:
    return bank.open_savings(alice, Decimal("1000.00"), annual_rate=Decimal("0.12"))


@pytest.fixture
def checking(bank: Bank, alice: Customer) -> CheckingAccount:
    return bank.open_checking(
        alice, Decimal("500.00"), overdraft_limit=Decimal("100.00")
    )


# ---------------------------------------------------------------------------
# Transaction dataclass
# ---------------------------------------------------------------------------

def test_transaction_is_frozen() -> None:
    txn = Transaction(
        id="abc", type="deposit", amount=Decimal("10"),
        balance_after=Decimal("110"), timestamp=__import__("datetime").datetime.utcnow()
    )
    with pytest.raises(Exception):  # FrozenInstanceError
        txn.amount = Decimal("99")  # type: ignore[misc]


def test_transaction_make_id_unique() -> None:
    ids = {Transaction.make_id() for _ in range(100)}
    assert len(ids) == 100


# ---------------------------------------------------------------------------
# SavingsAccount — deposit
# ---------------------------------------------------------------------------

def test_savings_initial_deposit(savings: SavingsAccount) -> None:
    assert savings.balance == Decimal("1000.00")


def test_savings_deposit_increases_balance(savings: SavingsAccount) -> None:
    savings.deposit(Decimal("250.00"))
    assert savings.balance == Decimal("1250.00")


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-1"), Decimal("-100")])
def test_savings_deposit_non_positive_raises(
    savings: SavingsAccount, amount: Decimal
) -> None:
    with pytest.raises(NegativeAmountError):
        savings.deposit(amount)


# ---------------------------------------------------------------------------
# SavingsAccount — withdraw
# ---------------------------------------------------------------------------

def test_savings_withdraw_decreases_balance(savings: SavingsAccount) -> None:
    savings.withdraw(Decimal("200.00"))
    assert savings.balance == Decimal("800.00")


def test_savings_withdraw_exact_balance(savings: SavingsAccount) -> None:
    savings.withdraw(Decimal("1000.00"))
    assert savings.balance == Decimal("0.00")


def test_savings_withdraw_overdraft_raises(savings: SavingsAccount) -> None:
    with pytest.raises(InsufficientFundsError):
        savings.withdraw(Decimal("1001.00"))


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-50")])
def test_savings_withdraw_non_positive_raises(
    savings: SavingsAccount, amount: Decimal
) -> None:
    with pytest.raises(NegativeAmountError):
        savings.withdraw(amount)


# ---------------------------------------------------------------------------
# SavingsAccount — interest
# ---------------------------------------------------------------------------

def test_savings_apply_interest(savings: SavingsAccount) -> None:
    """12% annual → 1% monthly → $10.00 on $1000."""
    txn = savings.apply_interest()
    assert txn is not None
    assert txn.type == "interest"
    assert txn.amount == Decimal("10.00")
    assert savings.balance == Decimal("1010.00")


def test_savings_interest_no_txn_when_zero(bank: Bank, alice: Customer) -> None:
    acc = bank.open_savings(alice, Decimal("0"))
    txn = acc.apply_interest()
    assert txn is None


# ---------------------------------------------------------------------------
# CheckingAccount — overdraft
# ---------------------------------------------------------------------------

def test_checking_overdraft_allowed(checking: CheckingAccount) -> None:
    """Can go negative up to overdraft_limit."""
    checking.withdraw(Decimal("600.00"))  # balance = -100 (limit is -100)
    assert checking.balance == Decimal("-100.00")


def test_checking_overdraft_exceeded_raises(checking: CheckingAccount) -> None:
    with pytest.raises(InsufficientFundsError):
        checking.withdraw(Decimal("601.00"))  # would be -101 > limit


def test_checking_monthly_fee(checking: CheckingAccount) -> None:
    txn = checking.apply_interest()
    assert txn is not None
    assert txn.type == "interest"
    assert txn.amount == Decimal("5.00")


# ---------------------------------------------------------------------------
# Transfer
# ---------------------------------------------------------------------------

def test_transfer_between_accounts(bank: Bank, alice: Customer) -> None:
    bob = bank.register_customer("Bob", "bob@test.com")
    src = bank.open_savings(alice, Decimal("500.00"))
    dst = bank.open_savings(bob, Decimal("100.00"))

    src.transfer_to(dst, Decimal("200.00"))

    assert src.balance == Decimal("300.00")
    assert dst.balance == Decimal("300.00")


def test_transfer_insufficient_funds_raises(bank: Bank, alice: Customer) -> None:
    bob = bank.register_customer("Bob", "bob@test.com")
    src = bank.open_savings(alice, Decimal("100.00"))
    dst = bank.open_savings(bob, Decimal("0.00"))
    with pytest.raises(InsufficientFundsError):
        src.transfer_to(dst, Decimal("101.00"))


def test_transfer_records_both_sides(bank: Bank, alice: Customer) -> None:
    bob = bank.register_customer("Bob", "bob@test.com")
    src = bank.open_savings(alice, Decimal("300.00"))
    dst = bank.open_savings(bob, Decimal("0.00"))
    debit, credit = src.transfer_to(dst, Decimal("150.00"))
    assert debit.type == "transfer_out"
    assert credit.type == "transfer_in"


# ---------------------------------------------------------------------------
# Customer
# ---------------------------------------------------------------------------

def test_customer_net_worth(bank: Bank, alice: Customer) -> None:
    bank.open_savings(alice, Decimal("1000.00"))
    bank.open_checking(alice, Decimal("500.00"))
    assert alice.net_worth() == Decimal("1500.00")


def test_customer_get_account_missing_raises(alice: Customer) -> None:
    with pytest.raises(KeyError):
        alice.get_account("NONEXISTENT")


def test_customer_monthly_statement_contains_name(
    bank: Bank, alice: Customer, savings: SavingsAccount
) -> None:
    stmt = alice.monthly_statement()
    assert "Alice" in stmt


# ---------------------------------------------------------------------------
# Bank
# ---------------------------------------------------------------------------

def test_bank_total_assets(bank: Bank, alice: Customer) -> None:
    bank.open_savings(alice, Decimal("1000.00"))
    bob = bank.register_customer("Bob", "bob@test.com")
    bank.open_savings(bob, Decimal("2000.00"))
    assert bank.total_assets() == Decimal("3000.00")


def test_bank_apply_all_interest(bank: Bank, alice: Customer) -> None:
    acc = bank.open_savings(alice, Decimal("1000.00"), annual_rate=Decimal("0.12"))
    bank.apply_all_interest()
    assert acc.balance > Decimal("1000.00")


def test_bank_csv_export_has_header(bank: Bank, alice: Customer) -> None:
    acc = bank.open_savings(alice, Decimal("100.00"))
    csv_str = bank.export_transactions_csv(acc)
    first_line = csv_str.splitlines()[0]
    assert "type" in first_line
    assert "amount" in first_line
