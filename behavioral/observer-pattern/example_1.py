"""Observer Pattern — Example 1: Stock Price Alerts.

A StockMarket subject notifies registered observers whenever a stock price
changes.  Different observers react differently: one logs trades, another
triggers buy/sell alerts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from observer_pattern import Observer, Subject


# ---------------------------------------------------------------------------
# Domain model
# ---------------------------------------------------------------------------

@dataclass
class StockMarket(Subject):
    """Publishes price updates for tracked stock symbols."""

    _prices: dict[str, float] = field(default_factory=dict, repr=False)

    def set_price(self, symbol: str, price: float) -> None:
        """Update *symbol* to *price* and notify observers."""
        self._prices[symbol] = price
        self.notify("price_update", {"symbol": symbol, "price": price})

    def get_price(self, symbol: str) -> float | None:
        """Return the current price for *symbol*, or ``None`` if unknown."""
        return self._prices.get(symbol)


# ---------------------------------------------------------------------------
# Observers
# ---------------------------------------------------------------------------

@dataclass
class TradeLogger(Observer):
    """Records every price update."""
    history: list[dict[str, Any]] = field(default_factory=list)

    def update(self, event: str, data: Any = None) -> None:
        if event == "price_update":
            self.history.append(data)
            print(f"[TradeLogger] {data['symbol']} → ${data['price']:.2f}")


@dataclass
class PriceAlertObserver(Observer):
    """Fires an alert when a price exceeds a configured threshold."""
    thresholds: dict[str, float] = field(default_factory=dict)
    triggered: list[str] = field(default_factory=list)

    def update(self, event: str, data: Any = None) -> None:
        if event != "price_update" or data is None:
            return
        sym, price = data["symbol"], data["price"]
        limit = self.thresholds.get(sym)
        if limit is not None and price >= limit:
            msg = f"{sym} hit ${price:.2f} (threshold ${limit:.2f})"
            self.triggered.append(msg)
            print(f"[PriceAlert] 🚨 {msg}")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    market = StockMarket()
    logger = TradeLogger()
    alert = PriceAlertObserver(thresholds={"AAPL": 190.0, "TSLA": 250.0})

    market.attach(logger)
    market.attach(alert)

    market.set_price("AAPL", 185.50)
    market.set_price("TSLA", 240.00)
    market.set_price("AAPL", 192.00)   # should trigger alert
    market.set_price("TSLA", 255.75)   # should trigger alert
    market.set_price("GOOG", 175.30)

    print("\n=== Trade History ===")
    for entry in logger.history:
        print(f"  {entry}")

    print("\n=== Triggered Alerts ===")
    for msg in alert.triggered:
        print(f"  {msg}")


if __name__ == "__main__":
    main()
