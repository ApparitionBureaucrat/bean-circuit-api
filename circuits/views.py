from __future__ import annotations

import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from pydantic import ValidationError

from .models import CircuitStop
from .schemas import CircuitCreate, CircuitResponse, ShopCreate, ShopResponse, StoryRequest
from .services import CircuitService, RouteStory


_service = CircuitService()


def _decode_payload(request: HttpRequest) -> dict:
    try:
        return json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError as error:
        raise ValueError("Invalid JSON payload") from error


def _error_payload(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"error": message}, status=status)


def shop_list_and_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        neighborhood = request.GET.get("neighborhood")
        payload = [
            ShopResponse.model_validate(shop).model_dump()
            for shop in _service.list_shops(neighborhood)
        ]
        return JsonResponse({"results": payload})

    if request.method == "POST":
        try:
            data = _decode_payload(request)
            payload = ShopCreate.model_validate(data)
            shop = _service.create_shop(**payload.model_dump())
        except (ValueError, ValidationError) as error:
            return _error_payload(str(error))
        return JsonResponse(ShopResponse.model_validate(shop).model_dump(), status=201)

    return _error_payload("Method not allowed", status=405)


def circuit_list_and_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        payload = [_circuit_to_payload(circuit) for circuit in _service.list_circuits()]
        return JsonResponse({"results": payload})

    if request.method == "POST":
        try:
            data = _decode_payload(request)
            request_payload = CircuitCreate.model_validate(data)
            circuit = _service.create_circuit(request_payload)
        except (ValueError, ValidationError) as error:
            return _error_payload(str(error))
        return JsonResponse(_circuit_to_payload(circuit), status=201)

    return _error_payload("Method not allowed", status=405)


def circuit_story_view(request: HttpRequest, circuit_id: int) -> HttpResponse:
    if request.method == "POST":
        try:
            circuit = _service.get_circuit(circuit_id)
            data = _decode_payload(request)
            request_payload = StoryRequest.model_validate(data)
            story = _service.generate_story_for_circuit(circuit, request_payload)
        except (ValueError, ValidationError) as error:
            return _error_payload(str(error))
        return _story_payload(story, circuit_id)

    if request.method == "GET":
        try:
            circuit = _service.get_circuit(circuit_id)
        except Exception as error:
            return _error_payload(str(error))
        return JsonResponse(_circuit_to_payload(circuit))

    return _error_payload("Method not allowed", status=405)


def _story_payload(story: RouteStory, circuit_id: int) -> JsonResponse:
    return JsonResponse(
        {
            "circuit_id": circuit_id,
            "text": story.text,
        }
    )


def _circuit_to_payload(circuit) -> dict:
    ordered_stops = list(
        CircuitStop.objects.filter(circuit=circuit)
        .select_related("shop")
        .order_by("position")
        .all()
    )
    shop_ids = [stop.shop_id for stop in ordered_stops]
    shop_names = [stop.shop.name for stop in ordered_stops]
    return CircuitResponse(
        id=circuit.id,
        name=circuit.name,
        neighborhood_focus=circuit.neighborhood_focus,
        shop_ids=shop_ids,
        shop_names=shop_names,
    ).model_dump()
