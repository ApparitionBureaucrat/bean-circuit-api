from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, Iterable, List

from django.db import transaction
from django.db.models import QuerySet

from .models import Circuit, CircuitStop, Shop
from .schemas import CircuitCreate, StoryRequest

try:
    from pydantic_ai import Agent
except Exception:  # pragma: no cover - optional integration surface
    Agent = None  # type: ignore[assignment]


@dataclass(frozen=True)
class RouteStory:
    """Normalized AI story response payload."""

    text: str


class CircuitService:
    """Business logic for listing and composing coffee circuits."""

    def list_shops(self, neighborhood: str | None = None) -> QuerySet[Shop]:
        queryset = Shop.objects.all()
        if neighborhood:
            queryset = queryset.filter(neighborhood__iexact=neighborhood)
        return queryset.order_by("name")

    def create_shop(
        self,
        name: str,
        neighborhood: str,
        address: str,
        signature_drink: str,
        notes: str = "",
    ) -> Shop:
        return Shop.objects.create(
            name=name,
            neighborhood=neighborhood,
            address=address,
            signature_drink=signature_drink,
            notes=notes,
        )

    def create_circuit(self, payload: CircuitCreate) -> Circuit:
        shops: List[Shop] = list(Shop.objects.filter(id__in=payload.shop_ids))
        if len(shops) != len(payload.shop_ids):
            existing_ids = {shop.id for shop in shops}
            missing = {shop_id for shop_id in payload.shop_ids if shop_id not in existing_ids}
            raise ValueError(f"Unknown shops referenced: {sorted(missing)}")

        with transaction.atomic():
            circuit = Circuit.objects.create(
                name=payload.name,
                neighborhood_focus=payload.neighborhood_focus,
            )
            stops = [
                CircuitStop(circuit=circuit, shop=shop, position=position)
                for position, shop in enumerate(shops, start=1)
            ]
            CircuitStop.objects.bulk_create(stops)
        return circuit

    def list_circuits(self) -> QuerySet[Circuit]:
        return Circuit.objects.prefetch_related("shops").order_by("-created_at")

    def get_circuit(self, circuit_id: int) -> Circuit:
        return Circuit.objects.get(id=circuit_id)

    def generate_story_for_circuit(self, circuit: Circuit, request: StoryRequest) -> RouteStory:
        story_input = self._build_story_prompt(circuit)
        generator = self._build_story_generator()
        if generator is None:
            text = self._fallback_story(circuit=circuit, mood=request.mood)
        else:
            text = generator(story_input, request.mood)
        return RouteStory(text=text)

    def _build_story_prompt(self, circuit: Circuit) -> str:
        shop_names = self._ordered_shop_names(circuit)
        if not shop_names:
            return (
                "Create a warm narrative about this neighborhood coffee circuit: "
                f"{circuit.name} in {circuit.neighborhood_focus}."
            )
        return (
            "Create a warm narrative about this neighborhood coffee circuit: "
            f"{circuit.name} in {circuit.neighborhood_focus}. "
            f"Include in order: {', '.join(shop_names)}."
        )

    def _ordered_shop_names(self, circuit: Circuit) -> List[str]:
        stops: Iterable[CircuitStop] = circuit.circuitstop_set.select_related("shop").order_by("position").all()
        return [stop.shop.name for stop in stops]

    def _build_story_generator(self) -> Callable[[str, str], str] | None:
        if Agent is None:
            return None

        model_name = os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o-mini")
        try:
            agent = Agent(
                model=model_name,
                system_prompt=(
                    "You are a coffee tourism copywriter. "
                    "Write concise route stories with a friendly and practical tone."
                ),
            )
        except Exception:
            return None

        def _generate_story(route_prompt: str, mood: str) -> str:
            try:
                result = agent.run_sync(f"{route_prompt} Mood: {mood}.")
                if hasattr(result, "data"):
                    return str(result.data)
                return str(result)
            except Exception:
                return self._fallback_story(route_prompt=route_prompt, mood=mood)

        return _generate_story

    def _fallback_story(
        self,
        circuit: Circuit | None = None,
        mood: str = "balanced",
        route_prompt: str | None = None,
    ) -> str:
        if route_prompt is None:
            if circuit is None:
                route_prompt = "A balanced coffee circuit through a local neighborhood."
            else:
                names = ", ".join(self._ordered_shop_names(circuit))
                route_prompt = (
                    f"A {mood} circuit through {circuit.neighborhood_focus}: "
                    f"{circuit.name} featuring {names}."
                )
        route_prompt = route_prompt.strip()
        return f"{route_prompt} A cup at each stop and a slow walk between them complete this route."
