"""pytest tests for metaclass idiom."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from metaclass import AppState, Plugin, PluginA, PluginB, Serializable, SingletonMeta, UserRecord


class TestSingletonMeta:
    def setup_method(self) -> None:
        SingletonMeta._instances.pop(AppState, None)

    def test_same_instance_returned(self) -> None:
        s1 = AppState()
        s2 = AppState()
        assert s1 is s2

    def test_shared_state(self) -> None:
        s1 = AppState()
        s1.counter = 99
        s2 = AppState()
        assert s2.counter == 99


class TestRegistryMeta:
    def test_base_class_not_in_registry(self) -> None:
        assert "Plugin" not in Plugin.registry

    def test_concrete_classes_registered(self) -> None:
        assert "PluginA" in Plugin.registry
        assert "PluginB" in Plugin.registry

    def test_registry_returns_correct_class(self) -> None:
        assert Plugin.registry["PluginA"] is PluginA
        assert Plugin.registry["PluginB"] is PluginB

    def test_new_subclass_auto_registered(self) -> None:
        class PluginTest(Plugin):
            def run(self) -> str:
                return "test"

        assert "PluginTest" in Plugin.registry

    def test_instantiated_plugin_runs(self) -> None:
        plugin = Plugin.registry["PluginA"]()
        assert plugin.run() == "PluginA output"


class TestInitSubclass:
    def test_valid_subclass_created(self) -> None:
        u = UserRecord(1, "Alice")
        assert u.name == "Alice"

    def test_schema_stored(self) -> None:
        assert UserRecord.schema == {"id": int, "name": str}

    def test_serialize_returns_dict(self) -> None:
        u = UserRecord(2, "Bob")
        result = u.serialize()
        assert result == {"id": 2, "name": "Bob"}

    def test_missing_schema_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="schema"):
            class MissingSchema(Serializable):  # type: ignore[call-arg]
                pass

    def test_metaclass_enforces_constraint_at_class_creation(self) -> None:
        """The error must occur at class definition time, not instantiation."""
        with pytest.raises(TypeError):
            exec("class X(Serializable): pass", {"Serializable": Serializable})
