from __future__ import annotations

from django.urls import path

from .views import circuit_list_and_create_view, circuit_story_view, shop_list_and_create_view

urlpatterns = [
    path("v1/shops/", shop_list_and_create_view, name="shop-list-create"),
    path("v1/circuits/", circuit_list_and_create_view, name="circuit-list-create"),
    path("v1/circuits/<int:circuit_id>/story/", circuit_story_view, name="circuit-story"),
]
