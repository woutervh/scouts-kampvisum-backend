import logging

from django.db import models

from apps.camps.models import CampYear

logger = logging.getLogger(__name__)


class CampVisumQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CampVisumManager(models.Manager):
    """
    Loads Category instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CampVisumQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        
        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass
        
        return None
