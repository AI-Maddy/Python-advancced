"""
Facade Pattern.

HomeTheaterFacade presents a simple ``watch_movie()`` / ``end_movie()``
interface that hides the complexity of orchestrating Amplifier, DVDPlayer,
Projector, and Lights subsystems.
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# Subsystems
# ---------------------------------------------------------------------------
class Amplifier:
    """Audio amplifier subsystem."""

    def __init__(self) -> None:
        self._volume = 0
        self._on = False

    def on(self) -> str:
        self._on = True
        return "Amplifier: on"

    def off(self) -> str:
        self._on = False
        return "Amplifier: off"

    def set_volume(self, level: int) -> str:
        self._volume = level
        return f"Amplifier: volume={level}"

    def set_surround_sound(self) -> str:
        return "Amplifier: 5.1 surround mode"


class DVDPlayer:
    """DVD/Blu-ray player subsystem."""

    def __init__(self) -> None:
        self._title: str = ""

    def on(self) -> str:
        return "DVDPlayer: on"

    def off(self) -> str:
        return "DVDPlayer: off"

    def play(self, movie: str) -> str:
        self._title = movie
        return f"DVDPlayer: playing '{movie}'"

    def stop(self) -> str:
        title = self._title
        self._title = ""
        return f"DVDPlayer: stopped '{title}'"


class Projector:
    """Video projector subsystem."""

    def on(self) -> str:
        return "Projector: on"

    def off(self) -> str:
        return "Projector: off"

    def wide_screen_mode(self) -> str:
        return "Projector: 16:9 widescreen"


class Lights:
    """Smart lighting subsystem."""

    def __init__(self) -> None:
        self._level = 100

    def dim(self, level: int) -> str:
        self._level = level
        return f"Lights: dimmed to {level}%"

    def on(self) -> str:
        self._level = 100
        return "Lights: on (100%)"


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------
class HomeTheaterFacade:
    """Simplified interface to the home-theater subsystems.

    Args:
        amp: Amplifier subsystem.
        dvd: DVDPlayer subsystem.
        projector: Projector subsystem.
        lights: Lights subsystem.
    """

    def __init__(
        self,
        amp: Amplifier,
        dvd: DVDPlayer,
        projector: Projector,
        lights: Lights,
    ) -> None:
        self._amp = amp
        self._dvd = dvd
        self._projector = projector
        self._lights = lights
        self._log: list[str] = []

    def watch_movie(self, movie: str) -> list[str]:
        """Orchestrate all subsystems to start the movie experience.

        Args:
            movie: Title of the movie to play.

        Returns:
            Ordered list of subsystem actions taken.
        """
        steps = [
            self._lights.dim(10),
            self._amp.on(),
            self._amp.set_surround_sound(),
            self._amp.set_volume(20),
            self._projector.on(),
            self._projector.wide_screen_mode(),
            self._dvd.on(),
            self._dvd.play(movie),
        ]
        self._log.extend(steps)
        return steps

    def end_movie(self) -> list[str]:
        """Shut down all subsystems after the movie ends.

        Returns:
            Ordered list of subsystem actions taken.
        """
        steps = [
            self._lights.on(),
            self._dvd.stop(),
            self._dvd.off(),
            self._projector.off(),
            self._amp.off(),
        ]
        self._log.extend(steps)
        return steps

    @property
    def log(self) -> list[str]:
        """All actions ever performed through this facade."""
        return list(self._log)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    theater = HomeTheaterFacade(
        Amplifier(), DVDPlayer(), Projector(), Lights()
    )
    print("=== Starting movie ===")
    for step in theater.watch_movie("Inception"):
        print(f"  {step}")

    print("\n=== Ending movie ===")
    for step in theater.end_movie():
        print(f"  {step}")
