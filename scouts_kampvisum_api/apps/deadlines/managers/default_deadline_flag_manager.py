import logging

from django.db import models

logger = logging.getLogger(__name__)


class DefaultDeadlineFlagQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DefaultDeadlineFlagManager(models.Manager):
    def get_queryset(self):
        return DefaultDeadlineFlagQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        default_deadline = kwargs.get("default_deadline", None)
        name = kwargs.get("name", None)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if default_deadline and name:
            try:
                return self.get_queryset().get(
                    default_deadline=default_deadline, name=name
                )
            except:
                pass

        return None
