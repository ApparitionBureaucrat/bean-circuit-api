from __future__ import annotations

import pytest

from circuits.schemas import CircuitCreate, ShopCreate, StoryRequest


def test_shop_create_rejects_short_name() -> None:
    with pytest.raises(ValueError):
        ShopCreate(name="A", neighborhood="Downtown", address="123 High Street", signature_drink="Latte")


def test_shop_create_accepts_minimal_payload() -> None:
    payload = ShopCreate(
        name="Brew Brothers",
        neighborhood="Riverside",
        address="101 Bean Ave",
        signature_drink="Pour-Over",
        notes="",
    )
    assert payload.name == "Brew Brothers"


def test_circuit_requires_at_least_two_stops() -> None:
    with pytest.raises(ValueError):
        CircuitCreate(name="Weekend Loop", neighborhood_focus="Riverside", shop_ids=[1])


def test_story_request_defaults() -> None:
    payload = StoryRequest()
    assert payload.mood == "balanced"
