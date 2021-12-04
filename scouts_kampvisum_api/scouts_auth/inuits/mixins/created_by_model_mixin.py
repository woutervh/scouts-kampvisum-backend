from django.db import models
from django.conf import settings


class CreatedByModelMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
