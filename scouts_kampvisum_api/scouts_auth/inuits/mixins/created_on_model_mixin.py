from django.db import models
from django.utils import timezone


class CreatedOnModelMixin(models.Model):
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
