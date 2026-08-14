from django.conf import settings
from django.db import models
from django.utils import timezone

from common.models import BaseModel


class Policy(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        ACTIVE = "active", "Activo"
        EXPIRED = "expired", "Vencido"
        CANCELLED = "cancelled", "Cancelado"

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
    sequence_number = models.AutoField(unique=True, editable=False)
    policy_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["pet"],
                condition=models.Q(status="active"),
                name="unique_active_policy_per_pet",
            )
        ]

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            year = timezone.now().year
            formatted_sequence = f"{self.sequence_number:05d}"
            self.policy_number = f"PG-{year}-{formatted_sequence}"
            super().save(update_fields=["policy_number"])

    def __str__(self):
        return self.policy_number
