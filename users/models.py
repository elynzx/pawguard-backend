import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None
    email = models.EmailField(unique=True)
    dni = models.CharField(max_length=8, unique=True)
    phone = models.CharField(max_length=9)
    address = models.CharField(max_length=300)

    district = models.ForeignKey(
        "locations.District",
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
    )

    account_activated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    def __str__(self):
        return self.email
