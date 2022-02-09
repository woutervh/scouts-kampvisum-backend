import logging

from django.db import models


logger = logging.getLogger(__name__)


class DefaultDeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DefaultDeadlineManager(models.Manager):
    def get_queryset(self):
        return DefaultDeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        return None

    def get_by_natural_key(self, name, deadline_type):
        logger.debug(
            "GET BY NATURAL KEY %s: (name: %s (%s), deadline_type: %s (%s))",
            "DefaultDeadline",
            name,
            type(name).__name__,
            deadline_type,
            type(deadline_type).__name__,
        )

        return self.get(name=name, deadline_type=deadline_type)
