"""
Example 1 — UI widget tree.

A window contains panels, which contain buttons and labels.
All are treated uniformly via the Component interface.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Widget(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def render(self, indent: int = 0) -> str: ...

    def add(self, widget: Widget) -> None:
        raise NotImplementedError

    def remove(self, widget: Widget) -> None:
        raise NotImplementedError


class Button(Widget):
    def __init__(self, name: str, label: str) -> None:
        super().__init__(name)
        self.label = label

    def render(self, indent: int = 0) -> str:
        return " " * indent + f"[Button: {self.label}]"


class Label(Widget):
    def __init__(self, name: str, text: str) -> None:
        super().__init__(name)
        self.text = text

    def render(self, indent: int = 0) -> str:
        return " " * indent + f"<Label: {self.text}>"


class Panel(Widget):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[Widget] = []

    def add(self, widget: Widget) -> None:
        self._children.append(widget)

    def remove(self, widget: Widget) -> None:
        self._children.remove(widget)

    def render(self, indent: int = 0) -> str:
        lines = [" " * indent + f"Panel({self.name}) {{"]
        for child in self._children:
            lines.append(child.render(indent + 2))
        lines.append(" " * indent + "}")
        return "\n".join(lines)


def main() -> None:
    window = Panel("main-window")
    toolbar = Panel("toolbar")
    content = Panel("content")

    toolbar.add(Button("btn-save", "Save"))
    toolbar.add(Button("btn-open", "Open"))
    toolbar.add(Button("btn-close", "Close"))

    content.add(Label("lbl-title", "Hello, World!"))
    content.add(Button("btn-ok", "OK"))

    window.add(toolbar)
    window.add(content)

    print(window.render())


if __name__ == "__main__":
    main()
