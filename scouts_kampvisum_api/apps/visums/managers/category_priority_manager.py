from django.db import models


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CategoryPriorityQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CategoryPriorityManager(models.Manager):
    def get_queryset(self):
        return CategoryPriorityQuerySet(self.model, using=self._db)

    def get_highest_priority(self):
        return self.get_queryset().order_by("priority").first()

    def get_by_natural_key(self, owner):
        logger.trace(
            "GET BY NATURAL KEY %s: (owner: %s (%s))",
            "CategoryPriority",
            owner,
            type(owner).__name__,
        )
        return self.get(owner=owner)
