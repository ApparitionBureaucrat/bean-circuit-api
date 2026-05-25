from __future__ import annotations

from circuits.services import CircuitService


def test_fallback_story_uses_prompt_override() -> None:
    service = CircuitService()
    story = service._fallback_story(route_prompt="A playful dawn circuit", mood="playful")
    assert "A playful dawn circuit" in story
    assert "A cup at each stop" in story
