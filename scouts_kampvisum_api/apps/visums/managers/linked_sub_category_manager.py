import logging

from django.db import models


logger = logging.getLogger(__name__)


class LinkedSubCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedSubCategoryManager(models.Manager):
    """
    Loads LinkedSubCategory instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedSubCategoryQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        
        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass
        
        return None
