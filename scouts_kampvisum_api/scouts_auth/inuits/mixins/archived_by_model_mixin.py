from django.db import models
from django.conf import settings


class ArchivedByModelMixin(models.Model):
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Archived by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_archived",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
