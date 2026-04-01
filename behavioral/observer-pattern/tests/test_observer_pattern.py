"""Tests for the Observer Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from observer_pattern import (
    AlertSystem,
    EventLogger,
    MetricsCollector,
    Observer,
    Subject,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class SimpleObserver(Observer):
    """Test double that records all calls."""
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def update(self, event: str, data: object = None) -> None:
        self.calls.append((event, data))


# ---------------------------------------------------------------------------
# Subject tests
# ---------------------------------------------------------------------------

class TestSubject:
    def test_attach_and_notify(self) -> None:
        sub = Subject()
        obs = SimpleObserver()
        sub.attach(obs)
        sub.notify("ping", 42)
        assert obs.calls == [("ping", 42)]

    def test_detach_stops_notifications(self) -> None:
        sub = Subject()
        obs = SimpleObserver()
        sub.attach(obs)
        sub.notify("a", 1)
        sub.detach(obs)
        sub.notify("b", 2)
        assert len(obs.calls) == 1

    def test_multiple_observers_all_notified(self) -> None:
        sub = Subject()
        o1, o2, o3 = SimpleObserver(), SimpleObserver(), SimpleObserver()
        for o in (o1, o2, o3):
            sub.attach(o)
        sub.notify("x", "data")
        for o in (o1, o2, o3):
            assert o.calls == [("x", "data")]

    def test_event_specific_attachment(self) -> None:
        sub = Subject()
        specific = SimpleObserver()
        wildcard = SimpleObserver()
        sub.attach(specific, "click")
        sub.attach(wildcard)           # receives all
        sub.notify("click", None)
        sub.notify("hover", None)
        # specific only gets click
        assert len(specific.calls) == 1
        # wildcard gets both
        assert len(wildcard.calls) == 2

    def test_duplicate_attach_is_idempotent(self) -> None:
        sub = Subject()
        obs = SimpleObserver()
        sub.attach(obs)
        sub.attach(obs)  # second attach should be a no-op
        sub.notify("dup", None)
        assert len(obs.calls) == 1

    def test_detach_nonexistent_does_not_raise(self) -> None:
        sub = Subject()
        obs = SimpleObserver()
        sub.detach(obs)  # should not raise

    def test_no_observers_notify_does_nothing(self) -> None:
        sub = Subject()
        sub.notify("empty")  # should not raise


# ---------------------------------------------------------------------------
# EventLogger tests
# ---------------------------------------------------------------------------

class TestEventLogger:
    def test_logs_events(self) -> None:
        logger = EventLogger()
        sub = Subject()
        sub.attach(logger)
        sub.notify("login", "user1")
        sub.notify("logout", "user1")
        assert logger.log == [("login", "user1"), ("logout", "user1")]

    def test_interface_contract(self) -> None:
        logger = EventLogger()
        assert isinstance(logger, Observer)


# ---------------------------------------------------------------------------
# MetricsCollector tests
# ---------------------------------------------------------------------------

class TestMetricsCollector:
    def test_counts_events(self) -> None:
        mc = MetricsCollector()
        sub = Subject()
        sub.attach(mc)
        sub.notify("click")
        sub.notify("click")
        sub.notify("submit")
        assert mc.counts["click"] == 2
        assert mc.counts["submit"] == 1

    def test_zero_count_before_event(self) -> None:
        mc = MetricsCollector()
        assert mc.counts.get("never") is None


# ---------------------------------------------------------------------------
# AlertSystem tests
# ---------------------------------------------------------------------------

class TestAlertSystem:
    def test_fires_on_watched_event(self) -> None:
        alert = AlertSystem(watched_events={"critical"})
        sub = Subject()
        sub.attach(alert)
        sub.notify("critical", "disk full")
        assert len(alert.alerts) == 1
        assert "critical" in alert.alerts[0]

    def test_ignores_unwatched_event(self) -> None:
        alert = AlertSystem(watched_events={"critical"})
        sub = Subject()
        sub.attach(alert)
        sub.notify("info", "all good")
        assert len(alert.alerts) == 0

    def test_empty_watched_events_fires_on_all(self) -> None:
        alert = AlertSystem()  # watched_events is empty set → all events
        sub = Subject()
        sub.attach(alert)
        sub.notify("anything", "payload")
        assert len(alert.alerts) == 1
