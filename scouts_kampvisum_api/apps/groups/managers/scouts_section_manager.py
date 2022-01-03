import logging

from django.db import models


logger = logging.getLogger(__name__)


class ScoutsSectionManager(models.Manager):
    def get_by_natural_key(self, group_admin_id):
        logger.debug(
            "GET BY NATURAL KEY %s: (group_admin_id: %s (%s))",
            "ScoutsSection",
            group_admin_id,
            type(group_admin_id).__name__,
        )
        return self.get(group_admin_id=group_admin_id)
