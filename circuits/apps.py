from __future__ import annotations

from django.apps import AppConfig


class CircuitsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    default = True
    name = "circuits"
