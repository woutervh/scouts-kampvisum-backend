import logging

from django.db import models
from django.db.models import Q
from django.conf import settings

logger = logging.getLogger(__name__)


class DeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineManager(models.Manager):
    def get_queryset(self):
        return DeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        return None
    
    def list_for_visum(self, *args, **kwargs):
        visum = kwargs.get("visum", None)
        
        if visum:
            return self.get_queryset().filter(visum=visum)
        
        return None
