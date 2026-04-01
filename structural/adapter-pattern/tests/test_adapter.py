"""pytest tests for adapter pattern."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from adapter import Adaptee, ClassAdapter, ObjectAdapter, Target, client_code


class TestObjectAdapter:
    def setup_method(self) -> None:
        self.adaptee = Adaptee()
        self.adapter = ObjectAdapter(self.adaptee)

    def test_adapter_is_target(self) -> None:
        assert isinstance(self.adapter, Target)

    def test_request_translates_correctly(self) -> None:
        result = self.adapter.request()
        assert result == "This is the response of the Adaptee!"

    def test_client_code_works(self) -> None:
        result = client_code(self.adapter)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_compute_delegates_to_adaptee(self) -> None:
        assert self.adapter.compute(3, 4) == 3 * 4 + 42

    def test_wraps_adaptee_instance(self) -> None:
        assert self.adapter._adaptee is self.adaptee


class TestClassAdapter:
    def setup_method(self) -> None:
        self.adapter = ClassAdapter()

    def test_adapter_is_target(self) -> None:
        assert isinstance(self.adapter, Target)

    def test_adapter_is_also_adaptee(self) -> None:
        assert isinstance(self.adapter, Adaptee)

    def test_request_translates_correctly(self) -> None:
        result = self.adapter.request()
        assert result == "This is the response of the Adaptee!"

    def test_client_code_works(self) -> None:
        result = client_code(self.adapter)
        assert isinstance(result, str)


class TestAdapteeRaw:
    def test_specific_request_is_reversed(self) -> None:
        adaptee = Adaptee()
        raw = adaptee.specific_request()
        assert raw == raw[::-1][::-1]  # double-reversed = original

    def test_legacy_compute(self) -> None:
        adaptee = Adaptee()
        assert adaptee.legacy_compute(5, 5) == 67
