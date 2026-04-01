"""pytest tests for mixin idiom."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from mixin_idiom import (
    AuditedUser,
    Entity,
    LoggingMixin,
    SerializationMixin,
    User,
    ValidationMixin,
    show_mro,
)


class TestLoggingMixin:
    def test_logger_attribute(self) -> None:
        import logging
        u = User(1, "Alice", 30)
        assert isinstance(u.logger, logging.Logger)

    def test_log_does_not_raise(self) -> None:
        u = User(1, "Alice", 30)
        u.log("info", "test message")  # should not raise


class TestValidationMixin:
    def test_valid_user_passes(self) -> None:
        u = User(1, "Alice", 30)
        u.validate()  # no exception

    def test_empty_name_fails(self) -> None:
        u = User(1, "", 30)
        with pytest.raises(ValueError, match="name"):
            u.validate()

    def test_negative_age_fails(self) -> None:
        u = User(1, "Alice", -1)
        with pytest.raises(ValueError, match="age"):
            u.validate()


class TestSerializationMixin:
    def test_to_json_returns_string(self) -> None:
        u = User(1, "Alice", 30)
        assert isinstance(u.to_json(), str)

    def test_json_contains_fields(self) -> None:
        import json
        u = User(1, "Alice", 30)
        d = json.loads(u.to_json())
        assert d["name"] == "Alice"
        assert d["age"] == 30

    def test_from_json_round_trip(self) -> None:
        u = User(1, "Bob", 25)
        restored = User.from_json(u.to_json())
        assert restored.name == "Bob"
        assert restored.age == 25


class TestUserCombined:
    def test_user_has_all_mixin_methods(self) -> None:
        u = User(1, "Alice", 30)
        assert hasattr(u, "log")
        assert hasattr(u, "validate")
        assert hasattr(u, "to_json")

    def test_save_calls_validate(self) -> None:
        u = User(1, "", 30)
        with pytest.raises(ValueError):
            u.save()


class TestMRO:
    def test_user_mro_contains_mixins(self) -> None:
        mro = show_mro(User)
        assert "LoggingMixin" in mro
        assert "ValidationMixin" in mro
        assert "SerializationMixin" in mro
        assert "Entity" in mro

    def test_user_mro_order(self) -> None:
        mro = show_mro(User)
        # LoggingMixin before ValidationMixin
        assert mro.index("LoggingMixin") < mro.index("ValidationMixin")

    def test_audited_user_mro_contains_user(self) -> None:
        mro = show_mro(AuditedUser)
        assert "User" in mro

    def test_object_appears_last(self) -> None:
        mro = show_mro(User)
        assert mro[-1] == "object"


class TestAuditedUser:
    def test_audit_log_populated(self) -> None:
        au = AuditedUser(1, "Carol", 28)
        au.save()
        assert len(au.audit_log) == 1
        assert "save" in au.audit_log[0]

    def test_cooperative_super(self) -> None:
        """save() in AuditedUser must also call User.save via super()."""
        au = AuditedUser(1, "Carol", 28)
        au.save()  # should not raise; proves User.save() was called
