"""Tests for the Template Method Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from template_method_pattern import (
    CSVProcessor,
    DataProcessor,
    JSONProcessor,
    XMLProcessor,
)


class TestCSVProcessor:
    def test_process_runs_full_pipeline(self) -> None:
        proc = CSVProcessor(["a, b, c"])
        proc.process()
        assert proc.result == ["A,B,C"]

    def test_strips_whitespace(self) -> None:
        proc = CSVProcessor(["  hello ,  world  "])
        proc.process()
        assert proc.result == ["HELLO,WORLD"]

    def test_multiple_rows(self) -> None:
        proc = CSVProcessor(["a,b", "c,d"])
        proc.process()
        assert proc.result == ["A,B", "C,D"]

    def test_empty_input(self) -> None:
        proc = CSVProcessor([])
        proc.process()
        assert proc.result == []


class TestJSONProcessor:
    def test_projects_requested_keys(self) -> None:
        records = [{"id": 1, "name": "Alice", "secret": "x"}]
        proc = JSONProcessor(records, keep_keys=["id", "name"])
        proc.process()
        assert proc.result == [{"id": 1, "name": "Alice"}]

    def test_missing_keys_ignored(self) -> None:
        records = [{"id": 1}]
        proc = JSONProcessor(records, keep_keys=["id", "name"])
        proc.process()
        assert proc.result == [{"id": 1}]

    def test_empty_records(self) -> None:
        proc = JSONProcessor([], keep_keys=["id"])
        proc.process()
        assert proc.result == []


class TestXMLProcessor:
    def test_output_contains_root_tag(self) -> None:
        proc = XMLProcessor([("name", "Alice")])
        proc.process()
        assert "<root>" in proc.output
        assert "</root>" in proc.output

    def test_output_contains_element(self) -> None:
        proc = XMLProcessor([("city", "Paris")])
        proc.process()
        assert "<city>Paris</city>" in proc.output

    def test_multiple_elements(self) -> None:
        elements = [("a", "1"), ("b", "2"), ("c", "3")]
        proc = XMLProcessor(elements)
        proc.process()
        for tag, val in elements:
            assert f"<{tag}>{val}</{tag}>" in proc.output


class TestHooksCalledInOrder:
    """Verify that template method calls hooks in the correct order."""

    def test_hooks_called_in_order(self) -> None:
        call_order: list[str] = []

        class TrackingProcessor(DataProcessor):
            def before_process(self) -> None:
                call_order.append("before")

            def read(self):
                call_order.append("read")
                return []

            def transform(self, data):
                call_order.append("transform")
                return data

            def write(self, data) -> None:
                call_order.append("write")

            def after_process(self) -> None:
                call_order.append("after")

        TrackingProcessor().process()
        assert call_order == ["before", "read", "transform", "write", "after"]

    def test_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            DataProcessor()  # type: ignore[abstract]

    def test_interface_contract(self) -> None:
        for ProcessorClass in (CSVProcessor, JSONProcessor, XMLProcessor):
            assert issubclass(ProcessorClass, DataProcessor)
