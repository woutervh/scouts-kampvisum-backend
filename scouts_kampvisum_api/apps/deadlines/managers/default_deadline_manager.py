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
        name = kwargs.get("name", None)
        deadline_type = kwargs.get("deadline_type", None)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if name and deadline_type:
            try:
                return self.get_queryset().get(name=name, deadline_type=deadline_type)
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
