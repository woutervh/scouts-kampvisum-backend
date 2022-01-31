import logging

from django.db import models


logger = logging.getLogger(__name__)


class CampTypeQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CampTypeManager(models.Manager):
    """
    Loads CampType instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CampTypeQuerySet(self.model, using=self._db)

    def get_by_natural_key(self, camp_type):
        logger.debug(
            "GET BY NATURAL KEY %s: (camp_type: %s (%s))",
            "CampType",
            camp_type,
            type(camp_type).__name__,
        )

        if camp_type.strip() == "*":
            logger.debug("ALL CAMP TYPES")

        return self.get(camp_type=camp_type)

    def get_default(self):
        return self.get_queryset().get(is_default=True)
