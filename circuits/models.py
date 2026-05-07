from __future__ import annotations

from django.db import models


class Shop(models.Model):
    """A neighborhood coffee shop participating in a bean circuit."""

    name = models.CharField(max_length=120)
    neighborhood = models.CharField(max_length=120)
    address = models.CharField(max_length=220)
    signature_drink = models.CharField(max_length=120)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "address"]

    def __str__(self) -> str:
        return f"{self.name} in {self.neighborhood}"


class Circuit(models.Model):
    """A curated route connecting multiple coffee shops."""

    name = models.CharField(max_length=150)
    neighborhood_focus = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    shops = models.ManyToManyField(
        Shop,
        through="CircuitStop",
        related_name="circuits",
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.neighborhood_focus})"


class CircuitStop(models.Model):
    """Ordered shop join table so circuits remain route-aware."""

    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["circuit", "position"]
        unique_together = ["circuit", "position"]
        indexes = [
            models.Index(fields=["circuit", "position"]),
        ]

    def __str__(self) -> str:
        return f"{self.circuit_id} stop {self.position}: {self.shop_id}"
