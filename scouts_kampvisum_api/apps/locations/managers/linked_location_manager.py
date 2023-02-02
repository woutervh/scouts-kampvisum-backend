from django.db import models
from django.conf import settings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedLocationQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedLocationManager(models.Manager):
    def get_queryset(self):
        return LinkedLocationQuerySet(self.model, using=self._db).prefetch_related('locations')

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        return None
