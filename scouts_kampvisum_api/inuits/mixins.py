from django.db import models
from django.conf import settings

# Mixins copied from werkwinkel project


class CreatedByMixin(models.Model):
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


class AuditTimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
