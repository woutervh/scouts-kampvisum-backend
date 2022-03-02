from django.db import models
from django.utils import timezone


class ArchivedOnModelMixin(models.Model):
    archived_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
