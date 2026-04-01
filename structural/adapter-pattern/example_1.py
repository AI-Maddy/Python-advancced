"""
Example 1 — Legacy payment gateway adapter.

LegacyPaymentGateway uses old-style method names.  PaymentAdapter presents
a clean modern interface to the rest of the application.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PaymentResult:
    success: bool
    transaction_id: str
    message: str


class PaymentProcessor(ABC):
    """Modern target interface."""

    @abstractmethod
    def charge(self, amount_cents: int, card_token: str) -> PaymentResult: ...

    @abstractmethod
    def refund(self, transaction_id: str) -> PaymentResult: ...


class LegacyPaymentGateway:
    """Old third-party SDK — cannot be modified."""

    def do_charge(self, amount: float, cc_number: str) -> dict:
        return {
            "status": "OK",
            "txn": f"TXN-{abs(hash(cc_number)) % 100000}",
            "msg": f"Charged ${amount:.2f}",
        }

    def cancel_charge(self, txn_ref: str) -> dict:
        return {"status": "OK", "txn": txn_ref, "msg": "Refunded"}


class LegacyPaymentAdapter(PaymentProcessor):
    """Adapts LegacyPaymentGateway to the modern PaymentProcessor interface."""

    def __init__(self, gateway: LegacyPaymentGateway) -> None:
        self._gw = gateway

    def charge(self, amount_cents: int, card_token: str) -> PaymentResult:
        result = self._gw.do_charge(amount_cents / 100.0, card_token)
        return PaymentResult(
            success=result["status"] == "OK",
            transaction_id=result["txn"],
            message=result["msg"],
        )

    def refund(self, transaction_id: str) -> PaymentResult:
        result = self._gw.cancel_charge(transaction_id)
        return PaymentResult(
            success=result["status"] == "OK",
            transaction_id=result["txn"],
            message=result["msg"],
        )


def checkout(processor: PaymentProcessor, amount_cents: int, token: str) -> None:
    result = processor.charge(amount_cents, token)
    if result.success:
        print(f"Payment OK: {result.transaction_id} — {result.message}")
    else:
        print(f"Payment FAILED: {result.message}")


def main() -> None:
    gateway = LegacyPaymentGateway()
    adapter = LegacyPaymentAdapter(gateway)
    checkout(adapter, 4999, "tok_visa_4242")
    r = adapter.refund("TXN-12345")
    print(f"Refund: {r.message}")


if __name__ == "__main__":
    main()
