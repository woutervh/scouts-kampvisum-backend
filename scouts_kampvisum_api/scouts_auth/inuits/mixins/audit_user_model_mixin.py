from django.db import models
from django.conf import settings


class AuditUserModelMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Instance created by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Instance last update by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_updated",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
