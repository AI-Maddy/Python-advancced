"""Template Method Pattern — Example 3: Build Pipeline.

Different language build pipelines (Python, Java, C++) share the
same pipeline: clean → compile → test → package.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class BuildResult:
    steps: list[str] = field(default_factory=list)
    success: bool = True

    def add(self, msg: str) -> None:
        self.steps.append(msg)
        print(f"  {msg}")


class BuildPipeline(ABC):
    """Abstract build pipeline — template method is ``build()``."""

    def build(self, project: str) -> BuildResult:
        """Template: clean → compile → test → package."""
        result = BuildResult()
        self.clean(project, result)
        self.compile(project, result)
        if result.success:
            self.test(project, result)
        if result.success:
            self.package(project, result)
        return result

    @abstractmethod
    def clean(self, project: str, result: BuildResult) -> None: ...
    @abstractmethod
    def compile(self, project: str, result: BuildResult) -> None: ...
    @abstractmethod
    def test(self, project: str, result: BuildResult) -> None: ...
    @abstractmethod
    def package(self, project: str, result: BuildResult) -> None: ...


class PythonBuildPipeline(BuildPipeline):
    def clean(self, project: str, result: BuildResult) -> None:
        result.add(f"[Python] Removing __pycache__ and .pyc files from {project}")

    def compile(self, project: str, result: BuildResult) -> None:
        result.add(f"[Python] Compiling {project} with py_compile...")

    def test(self, project: str, result: BuildResult) -> None:
        result.add(f"[Python] Running pytest on {project}")

    def package(self, project: str, result: BuildResult) -> None:
        result.add(f"[Python] Building wheel: {project}-1.0.0-py3-none-any.whl")


class JavaBuildPipeline(BuildPipeline):
    def clean(self, project: str, result: BuildResult) -> None:
        result.add(f"[Java] Running mvn clean for {project}")

    def compile(self, project: str, result: BuildResult) -> None:
        result.add(f"[Java] Running javac for {project}")

    def test(self, project: str, result: BuildResult) -> None:
        result.add(f"[Java] Running JUnit tests for {project}")

    def package(self, project: str, result: BuildResult) -> None:
        result.add(f"[Java] Creating {project}.jar")


class CppBuildPipeline(BuildPipeline):
    def clean(self, project: str, result: BuildResult) -> None:
        result.add(f"[C++] Removing build/ directory for {project}")

    def compile(self, project: str, result: BuildResult) -> None:
        result.add(f"[C++] Running cmake --build for {project}")

    def test(self, project: str, result: BuildResult) -> None:
        result.add(f"[C++] Running ctest for {project}")

    def package(self, project: str, result: BuildResult) -> None:
        result.add(f"[C++] Creating {project}.tar.gz")


def main() -> None:
    projects = [
        ("myapp", PythonBuildPipeline()),
        ("server", JavaBuildPipeline()),
        ("engine", CppBuildPipeline()),
    ]

    for name, pipeline in projects:
        print(f"\n=== Building {name} with {type(pipeline).__name__} ===")
        result = pipeline.build(name)
        print(f"  Build {'succeeded' if result.success else 'FAILED'} "
              f"({len(result.steps)} steps)")


if __name__ == "__main__":
    main()
