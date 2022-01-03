from django.db import models
from django.utils import timezone


class AuditTimestampModelMixin(models.Model):
    # created_on = models.DateTimeField(auto_now_add=True, default=timezone.now)
    # updated_on = models.DateTimeField(auto_now=True, default=timezone.now)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
