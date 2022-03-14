from django.db import models
from django.utils import timezone


class UpdatedOnModelMixin(models.Model):
    """Stores the datetime when the object was updated (field name: updated_on)"""

    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
