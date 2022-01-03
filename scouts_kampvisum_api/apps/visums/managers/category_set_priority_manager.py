import logging

from django.db import models


logger = logging.getLogger(__name__)


class CategorySetPriorityManager(models.Manager):
    def get_by_natural_key(self, owner):
        logger.debug(
            "GET BY NATURAL KEY %s: (owner: %s (%s))",
            "CategorySetPriority",
            owner,
            type(owner).__name__,
        )
        return self.get(owner=owner)
