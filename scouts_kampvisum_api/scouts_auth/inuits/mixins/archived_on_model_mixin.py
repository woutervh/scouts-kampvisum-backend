from django.db import models
from django.utils import timezone


class ArchivedOnModelMixin(models.Model):
    """Stores the datetime when the object was archived (field name: archived_on)"""

    archived_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
