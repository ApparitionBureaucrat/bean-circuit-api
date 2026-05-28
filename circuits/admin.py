from __future__ import annotations

from django.contrib import admin

from .models import Circuit, CircuitStop, Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "neighborhood", "signature_drink")
    search_fields = ("name", "neighborhood")


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "neighborhood_focus", "created_at")
    list_filter = ("neighborhood_focus",)


admin.site.register(CircuitStop)
