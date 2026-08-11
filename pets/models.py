from django.conf import settings
from django.db import models

from common.models import BaseModel


class Pet(BaseModel):
    class PetSpecies(models.TextChoices):
        DOG = "dog", "Perro"
        CAT = "cat", "Gato"

    class PetGender(models.TextChoices):
        MALE = "male", "Macho"
        FEMALE = "female", "Hembra"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pets",
    )

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=3, choices=PetSpecies.choices)
    gender = models.CharField(max_length=6, choices=PetGender.choices, blank=True)
    breed = models.CharField(max_length=100, blank=True)
    is_companion_animal = models.BooleanField(default=False)
    photo_url = models.URLField(blank=True)

    declared_age_months = models.PositiveIntegerField(
        help_text="Edad aproximada de la mascota en meses.",
    )

    def __str__(self):
        return self.name
