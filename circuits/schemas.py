from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from typing import List


class ShopCreate(BaseModel):
    """Payload for creating a coffee shop."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=2, max_length=120)
    neighborhood: str = Field(min_length=2, max_length=120)
    address: str = Field(min_length=5, max_length=220)
    signature_drink: str = Field(min_length=2, max_length=120)
    notes: str = ""


class ShopResponse(BaseModel):
    """Public shop representation used by API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    neighborhood: str
    address: str
    signature_drink: str
    notes: str


class CircuitCreate(BaseModel):
    """Payload for creating a route circuit."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3, max_length=150)
    neighborhood_focus: str = Field(min_length=2, max_length=120)
    shop_ids: List[int] = Field(min_length=2)


class CircuitResponse(BaseModel):
    """Shape of circuit data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    neighborhood_focus: str
    shop_ids: List[int] = Field(default_factory=list)
    shop_names: List[str] = Field(default_factory=list)


class StoryRequest(BaseModel):
    """Input for generating an AI route story."""

    model_config = ConfigDict(extra="forbid")

    mood: str = Field(default="balanced")


class StoryResponse(BaseModel):
    """AI-generated story attached to a circuit."""

    model_config = ConfigDict(from_attributes=True)

    text: str
    circuit_id: int
