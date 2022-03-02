from django.db import models
from django.utils import timezone


class UpdatedOnModelMixin(models.Model):
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
