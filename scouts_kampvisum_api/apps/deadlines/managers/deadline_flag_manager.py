import logging

from django.db import models

logger = logging.getLogger(__name__)


class DeadlineFlagQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineFlagManager(models.Manager):
    def get_queryset(self):
        return DeadlineFlagQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        deadline = kwargs.get("deadline", None)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if parent and deadline:
            try:
                return self.get_queryset().get(parent=parent, deadline=deadline)
            except:
                pass

        return None
