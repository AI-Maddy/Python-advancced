"""
Example 1 — Particle system flyweight.

Thousands of particles share type descriptors (color, texture, shape).
Only their position and velocity (extrinsic) differ.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class ParticleType:
    """Shared intrinsic state for a class of particles."""
    name: str
    color: str
    texture: str
    shape: str

    def draw(self, x: float, y: float, vx: float, vy: float) -> str:
        return (
            f"{self.name}[{self.color}/{self.shape}] "
            f"pos=({x:.1f},{y:.1f}) vel=({vx:.1f},{vy:.1f})"
        )


class ParticleTypeFactory:
    def __init__(self) -> None:
        self._cache: dict[str, ParticleType] = {}

    def get(self, name: str, color: str, texture: str, shape: str) -> ParticleType:
        if name not in self._cache:
            self._cache[name] = ParticleType(name, color, texture, shape)
        return self._cache[name]

    @property
    def size(self) -> int:
        return len(self._cache)


@dataclass
class Particle:
    """Combines extrinsic (pos/vel) with a shared ParticleType flyweight."""
    x: float
    y: float
    vx: float
    vy: float
    ptype: ParticleType

    def render(self) -> str:
        return self.ptype.draw(self.x, self.y, self.vx, self.vy)


def main() -> None:
    factory = ParticleTypeFactory()

    smoke = factory.get("Smoke", "gray", "smoke.png", "circle")
    fire = factory.get("Fire", "orange", "fire.png", "triangle")
    spark = factory.get("Spark", "yellow", "spark.png", "dot")

    rng = random.Random(42)
    particles = []
    for _ in range(500):
        ptype = rng.choice([smoke, fire, spark])
        p = Particle(
            x=rng.uniform(0, 800), y=rng.uniform(0, 600),
            vx=rng.uniform(-5, 5), vy=rng.uniform(-5, 5),
            ptype=ptype,
        )
        particles.append(p)

    print(f"Particles: {len(particles)}, unique types: {factory.size}")
    for p in particles[:3]:
        print(p.render())

    # Verify flyweight reuse
    same_smoke = factory.get("Smoke", "gray", "smoke.png", "circle")
    print(f"Same smoke flyweight: {smoke is same_smoke}")


if __name__ == "__main__":
    main()
