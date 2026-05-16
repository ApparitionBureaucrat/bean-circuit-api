from __future__ import annotations

from dataclasses import dataclass

from circuits.services import CircuitService


@dataclass
class FakeShop:
    id: int
    name: str


@dataclass
class FakeCircuit:
    id: int
    name: str
    neighborhood_focus: str
    shops: list[FakeShop]


def test_fallback_story_mentions_all_components() -> None:
    service = CircuitService()
    story = service._fallback_story(circuit=FakeCircuit(1, "Neighborhood Trail", "Midtown", []), mood="playful")
    assert "Neighborhood Trail" in story
    assert "playful" in story
