from django.db import models

from common.models import BaseModel


class District(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Clinic(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=9, blank=True)

    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name="clinics",
    )

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name