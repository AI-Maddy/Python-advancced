"""
Example 2 — Theme factory (dark / light).

Produces compatible Color, Font, and Icon objects for Dark and Light themes.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Color(ABC):
    @abstractmethod
    def background(self) -> str: ...

    @abstractmethod
    def foreground(self) -> str: ...


class Font(ABC):
    @abstractmethod
    def family(self) -> str: ...

    @abstractmethod
    def size(self) -> int: ...


class Icon(ABC):
    @abstractmethod
    def style(self) -> str: ...


@dataclass
class DarkColor(Color):
    def background(self) -> str:
        return "#1e1e1e"

    def foreground(self) -> str:
        return "#d4d4d4"


@dataclass
class LightColor(Color):
    def background(self) -> str:
        return "#ffffff"

    def foreground(self) -> str:
        return "#000000"


class DarkFont(Font):
    def family(self) -> str:
        return "JetBrains Mono"

    def size(self) -> int:
        return 14


class LightFont(Font):
    def family(self) -> str:
        return "Segoe UI"

    def size(self) -> int:
        return 12


class DarkIcon(Icon):
    def style(self) -> str:
        return "outlined-white"


class LightIcon(Icon):
    def style(self) -> str:
        return "filled-black"


class ThemeFactory(ABC):
    @abstractmethod
    def create_color(self) -> Color: ...

    @abstractmethod
    def create_font(self) -> Font: ...

    @abstractmethod
    def create_icon(self) -> Icon: ...


class DarkThemeFactory(ThemeFactory):
    def create_color(self) -> Color:
        return DarkColor()

    def create_font(self) -> Font:
        return DarkFont()

    def create_icon(self) -> Icon:
        return DarkIcon()


class LightThemeFactory(ThemeFactory):
    def create_color(self) -> Color:
        return LightColor()

    def create_font(self) -> Font:
        return LightFont()

    def create_icon(self) -> Icon:
        return LightIcon()


def render_ui(factory: ThemeFactory) -> None:
    color = factory.create_color()
    font = factory.create_font()
    icon = factory.create_icon()
    print(
        f"BG={color.background()} FG={color.foreground()} "
        f"Font={font.family()}:{font.size()} Icon={icon.style()}"
    )


def main() -> None:
    print("Dark theme:")
    render_ui(DarkThemeFactory())
    print("Light theme:")
    render_ui(LightThemeFactory())


if __name__ == "__main__":
    main()
