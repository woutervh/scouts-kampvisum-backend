import logging

from django.db import models


logger = logging.getLogger(__name__)


class LinkedCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedCategoryManager(models.Manager):
    """
    Loads LinkedSubCategory instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedCategoryQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        return None
