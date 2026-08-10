import uuid

from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        now = timezone.now()
        return self.update(
            deleted_at=now,
            updated_at=now,
        )


class SoftDeleteManager(models.Manager):
    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(
            self.model,
            using=self._db,
        ).filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        now = timezone.now()
        self.deleted_at = now
        self.updated_at = now
        self.save(update_fields=["deleted_at", "updated_at"])

    def restore(self):
        self.deleted_at = None
        self.updated_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    class Meta:
        abstract = True