from typing import ClassVar

from django.db import models

from common.models import BaseModel


class Plan(BaseModel):
    class PetSpecies(models.TextChoices):
        DOG = "dog", "Perro"
        CAT = "cat", "Gato"

    name = models.CharField(max_length=150)
    species = models.CharField(max_length=3, choices=PetSpecies.choices)
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    recommended = models.BooleanField(default=False)

    benefits = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["name", "species"],
                name="unique_plan_name_per_species",
            ),
            models.CheckConstraint(
                condition=models.Q(monthly_price__gt=0),
                name="plan_monthly_price_positive",
            ),
        ]

    def __str__(self):
        return self.name
