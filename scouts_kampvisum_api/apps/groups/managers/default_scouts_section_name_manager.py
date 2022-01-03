import logging

from django.db import models


logger = logging.getLogger(__name__)


class DefaultScoutsSectionNameManager(models.Manager):
    """
    Loads DefaultScoutsSectionName instances by their group type and name, not their id.

    This is useful for defining fixtures.
    """

    # def get_by_natural_key(self, type: ScoutsGroupType, name: ScoutsSectionName):
    def get_by_natural_key(self, group_type, name):
        logger.debug(
            "GET BY NATURAL KEY %s: (group_type: %s (%s), name: %s (%s))",
            "DefaultScoutsSectionName",
            group_type,
            type(group_type).__name__,
            name,
            type(name).__name__,
        )
        return self.get(group_type=group_type, name=name)
