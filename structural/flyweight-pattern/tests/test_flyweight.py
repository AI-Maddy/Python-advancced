"""pytest tests for flyweight pattern."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from flyweight import CharacterContext, CharacterStyle, FlyweightFactory


class TestFlyweightFactory:
    def setup_method(self) -> None:
        self.factory = FlyweightFactory()

    def test_same_key_returns_same_object(self) -> None:
        s1 = self.factory.get_style("Arial", "black", 12)
        s2 = self.factory.get_style("Arial", "black", 12)
        assert s1 is s2

    def test_different_key_returns_different_object(self) -> None:
        s1 = self.factory.get_style("Arial", "black", 12)
        s2 = self.factory.get_style("Arial", "red", 12)
        assert s1 is not s2

    def test_cache_size_grows_correctly(self) -> None:
        self.factory.get_style("Arial", "black", 12)
        self.factory.get_style("Arial", "black", 14)
        self.factory.get_style("Times", "black", 12)
        assert self.factory.cache_size == 3

    def test_duplicate_does_not_grow_cache(self) -> None:
        self.factory.get_style("Arial", "black", 12)
        self.factory.get_style("Arial", "black", 12)
        assert self.factory.cache_size == 1

    def test_list_styles(self) -> None:
        self.factory.get_style("Arial", "black", 12)
        self.factory.get_style("Times", "red", 14)
        styles = self.factory.list_styles()
        assert len(styles) == 2
        assert all(isinstance(s, CharacterStyle) for s in styles)


class TestCharacterStyle:
    def test_render_contains_char(self) -> None:
        style = CharacterStyle("Arial", "black", 12)
        result = style.render("A", 10, 20)
        assert "A" in result

    def test_render_contains_position(self) -> None:
        style = CharacterStyle("Arial", "black", 12)
        result = style.render("B", 30, 40)
        assert "30" in result
        assert "40" in result

    def test_render_contains_font(self) -> None:
        style = CharacterStyle("Helvetica", "blue", 16)
        result = style.render("C", 0, 0)
        assert "Helvetica" in result

    def test_is_hashable_frozen(self) -> None:
        style = CharacterStyle("Arial", "black", 12)
        s = {style}  # Must be hashable
        assert len(s) == 1


class TestCharacterContext:
    def test_render_delegates_to_style(self) -> None:
        style = CharacterStyle("Arial", "black", 12)
        ctx = CharacterContext("X", 5, 10, style)
        result = ctx.render()
        assert "X" in result
        assert "5" in result

    def test_many_contexts_share_one_style(self) -> None:
        factory = FlyweightFactory()
        style = factory.get_style("Mono", "green", 10)
        contexts = [
            CharacterContext(ch, i, 0, style)
            for i, ch in enumerate("hello")
        ]
        ids = {id(ctx.style) for ctx in contexts}
        assert len(ids) == 1  # all share the same flyweight
