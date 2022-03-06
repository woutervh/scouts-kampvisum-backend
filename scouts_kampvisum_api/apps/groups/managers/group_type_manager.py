from django.db import models


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroupTypeManager(models.Manager):
    """
    Loads scouts group type instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, group_type):
        logger.trace(
            "GET BY NATURAL KEY %s: (group_type: %s (%s))",
            "ScoutsGroupType",
            group_type,
            type(group_type).__name__,
        )
        return self.get(group_type=group_type)
