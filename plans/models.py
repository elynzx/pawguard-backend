from django.db import models

from common.models import BaseModel


class Plan(BaseModel):
    class PetSpecies(models.TextChoices):
        DOG = "dog", "perro"
        CAT = "cat", "Gato"

    name = models.CharField(max_length=150)
    species = models.CharField(max_length=3, choices=PetSpecies.choices)
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    annual_price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    recommended = models.BooleanField(default=False)

    entry_age_limit_months = models.PositiveIntegerField(
        help_text="Edad máxima en meses para acceder al plan.",
    )

    permanence_age_limit_months = models.PositiveIntegerField(
        help_text="Edad máxima en meses para permanecer en el plan.",
    )

    benefits = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
