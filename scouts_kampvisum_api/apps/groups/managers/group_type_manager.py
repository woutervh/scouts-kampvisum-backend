import logging

from django.db import models


logger = logging.getLogger(__name__)


class ScoutsGroupTypeManager(models.Manager):
    """
    Loads scouts group type instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, group_type):
        logger.debug(
            "GET BY NATURAL KEY %s: (group_type: %s (%s))",
            "ScoutsGroupType",
            group_type,
            type(group_type).__name__,
        )
        return self.get(group_type=group_type)
