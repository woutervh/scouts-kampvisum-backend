import logging

from django.db import models

logger = logging.getLogger(__name__)


class DeadlineDateQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineDateManager(models.Manager):
    def get_queryset(self):
        return DeadlineDateQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        default_deadline = kwargs.get("default_deadline", None)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if default_deadline:
            try:
                return self.get_queryset().get(default_deadline=default_deadline)
            except:
                pass

        return None

    def get_by_natural_key(self, default_deadline):
        logger.debug(
            "GET BY NATURAL KEY %s: (default_deadline: %s (%s))",
            "DeadlineDate",
            default_deadline,
            type(default_deadline).__name__,
        )

        return self.get(default_deadline=default_deadline)
