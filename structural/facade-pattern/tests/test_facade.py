"""pytest tests for facade pattern."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from facade import Amplifier, DVDPlayer, HomeTheaterFacade, Lights, Projector


class TestHomeTheaterFacade:
    def setup_method(self) -> None:
        self.amp = Amplifier()
        self.dvd = DVDPlayer()
        self.proj = Projector()
        self.lights = Lights()
        self.theater = HomeTheaterFacade(
            self.amp, self.dvd, self.proj, self.lights
        )

    def test_watch_movie_returns_list(self) -> None:
        result = self.theater.watch_movie("Dune")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_watch_movie_contains_expected_steps(self) -> None:
        steps = self.theater.watch_movie("Dune")
        combined = " ".join(steps)
        assert "Amplifier" in combined
        assert "DVDPlayer" in combined
        assert "Projector" in combined
        assert "Lights" in combined

    def test_watch_movie_lights_dimmed(self) -> None:
        steps = self.theater.watch_movie("Dune")
        assert any("dim" in s.lower() for s in steps)

    def test_watch_movie_plays_correct_title(self) -> None:
        steps = self.theater.watch_movie("Interstellar")
        assert any("Interstellar" in s for s in steps)

    def test_end_movie_returns_list(self) -> None:
        self.theater.watch_movie("Dune")
        result = self.theater.end_movie()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_end_movie_turns_lights_on(self) -> None:
        self.theater.watch_movie("Dune")
        steps = self.theater.end_movie()
        assert any("Lights" in s and "100" in s for s in steps)

    def test_end_movie_stops_and_turns_off_dvd(self) -> None:
        self.theater.watch_movie("Dune")
        steps = self.theater.end_movie()
        assert any("stopped" in s for s in steps)
        assert any("off" in s.lower() for s in steps)

    def test_correct_order_in_watch_movie(self) -> None:
        steps = self.theater.watch_movie("Dune")
        # Lights should be dimmed before DVD starts playing
        lights_idx = next(i for i, s in enumerate(steps) if "Lights" in s)
        dvd_idx = next(i for i, s in enumerate(steps) if "playing" in s)
        assert lights_idx < dvd_idx

    def test_log_accumulates_actions(self) -> None:
        self.theater.watch_movie("A")
        self.theater.end_movie()
        assert len(self.theater.log) > 0
