"""
Example 2 — Image loading proxy.

HighResImage is expensive to load.  ImageProxy defers loading until
display() is actually called (virtual proxy for images).
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def display(self) -> str: ...

    @abstractmethod
    def filename(self) -> str: ...


class HighResImage(Image):
    """The real, expensive-to-load image."""

    def __init__(self, path: str) -> None:
        self._path = path
        # Simulate slow disk load
        self._data = f"<pixels:{path}:{len(path) * 100}bytes>"
        print(f"  [HighResImage] Loaded {path} from disk")

    def display(self) -> str:
        return f"Displaying {self._path}: {self._data}"

    def filename(self) -> str:
        return self._path


class ImageProxy(Image):
    """Virtual proxy — real image only loaded when display() is called."""

    def __init__(self, path: str) -> None:
        self._path = path
        self._real: HighResImage | None = None

    def display(self) -> str:
        if self._real is None:
            self._real = HighResImage(self._path)
        return self._real.display()

    def filename(self) -> str:
        return self._path

    @property
    def is_loaded(self) -> bool:
        return self._real is not None


def main() -> None:
    print("Creating proxies (no disk access yet)…")
    images = [
        ImageProxy("wallpaper_4k.jpg"),
        ImageProxy("profile_photo.png"),
        ImageProxy("banner.webp"),
    ]
    print(f"Created {len(images)} proxies, none loaded yet")
    for img in images:
        print(f"  {img.filename()} loaded={img.is_loaded}")  # type: ignore[attr-defined]

    print("\nDisplaying first image:")
    print(images[0].display())

    print("\nDisplaying first image again (no reload):")
    print(images[0].display())


if __name__ == "__main__":
    main()
