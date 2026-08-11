from typing import ClassVar

from django.conf import settings
from django.db import models

from common.models import BaseModel


class Policy(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        ACTIVE = "active", "Activo"
        EXPIRED = "expired", "Vencido"
        CANCELLED = "cancelled", "Cancelado"

    class ContractPeriod(models.TextChoices):
        SEMIANNUAL = "semiannual", "Semestral"
        ANNUAL = "annual", "Anual"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="policies",
    )

    pet = models.ForeignKey(
        "pets.Pet",
        on_delete=models.PROTECT,
        related_name="policies",
    )

    plan = models.ForeignKey(
        "plans.Plan",
        on_delete=models.PROTECT,
        related_name="policies",
    )

    policy_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    contract_period = models.CharField(max_length=20, choices=ContractPeriod.choices)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering: ClassVar[list[str]] = ["-created_at"]
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["pet"],
                condition=models.Q(status="active"),
                name="unique_active_policy_per_pet",
            )
        ]

    def __str__(self):
        return self.policy_number
