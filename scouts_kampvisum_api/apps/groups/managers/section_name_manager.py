import logging

from django.db import models


logger = logging.getLogger(__name__)


class ScoutsSectionNameManager(models.Manager):
    """
    Loads ScoutsSectionName instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name):
        logger.debug(
            "GET BY NATURAL KEY %s: (name: %s (%s))",
            "ScoutsSectionName",
            name,
            type(name).__name__,
        )
        return self.get(name=name)
