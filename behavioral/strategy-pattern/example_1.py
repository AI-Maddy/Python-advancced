"""Strategy Pattern — Example 1: Payment Processing Strategies.

A checkout system supports multiple payment methods (credit card, PayPal,
cryptocurrency).  Each is a strategy; the checkout context is unaware of
the details.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Strategy interface
# ---------------------------------------------------------------------------

class PaymentStrategy(ABC):
    """Abstract payment strategy."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process a payment of *amount* and return a confirmation string."""


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

@dataclass
class CreditCardPayment(PaymentStrategy):
    """Pays by credit card."""
    card_number: str
    holder: str

    def pay(self, amount: float) -> str:
        masked = "*" * 12 + self.card_number[-4:]
        return f"Charged ${amount:.2f} to card {masked} ({self.holder})"


@dataclass
class PayPalPayment(PaymentStrategy):
    """Pays via PayPal."""
    email: str

    def pay(self, amount: float) -> str:
        return f"PayPal payment of ${amount:.2f} sent from {self.email}"


@dataclass
class CryptoPayment(PaymentStrategy):
    """Pays with cryptocurrency."""
    wallet_address: str
    currency: str = "BTC"

    def pay(self, amount: float) -> str:
        return (
            f"Crypto payment: {amount:.4f} {self.currency} "
            f"→ wallet {self.wallet_address[:8]}..."
        )


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------

@dataclass
class Checkout:
    """Checkout context that delegates to the selected payment strategy."""
    strategy: PaymentStrategy

    def process(self, amount: float) -> str:
        """Process *amount* using the current payment strategy."""
        return self.strategy.pay(amount)

    def switch_payment(self, strategy: PaymentStrategy) -> None:
        """Change payment strategy at runtime."""
        self.strategy = strategy


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    checkout = Checkout(strategy=CreditCardPayment("4111111111111234", "Alice"))
    print(checkout.process(99.99))

    checkout.switch_payment(PayPalPayment("alice@example.com"))
    print(checkout.process(49.50))

    checkout.switch_payment(CryptoPayment("1A2b3C4d5E6f7G8h9I0j"))
    print(checkout.process(0.0025))


if __name__ == "__main__":
    main()
