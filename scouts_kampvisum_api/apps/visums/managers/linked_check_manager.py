import logging

from django.db import models


logger = logging.getLogger(__name__)


class LinkedCheckQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedCheckManager(models.Manager):
    """
    Loads LinkedCheck instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedCheckQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        
        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass
        
        return None
