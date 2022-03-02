from django.db import models
from django.conf import settings


class UpdatedByModelMixin(models.Model):
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="updated by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_updated",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
