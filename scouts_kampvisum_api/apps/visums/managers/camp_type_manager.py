import logging

from django.db import models


logger = logging.getLogger(__name__)


class CampTypeManager(models.Manager):
    """
    Loads CampType instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, camp_type):
        logger.debug(
            "GET BY NATURAL KEY %s: (name: %s (%s))",
            "Check",
            camp_type,
            type(camp_type).__name__,
        )

        return self.get(camp_type)
