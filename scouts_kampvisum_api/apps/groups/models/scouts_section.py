from django.db import models

from apps.groups.models import ScoutsSectionName
from apps.groups.managers import ScoutsSectionManager


from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSection(AbstractBaseModel):
    """
    A model for a scouts section, linked to their scouts group and name.
    """

    objects = ScoutsSectionManager()

    group_group_admin_id = RequiredCharField(max_length=64)
    name = models.ForeignKey(ScoutsSectionName, on_delete=models.DO_NOTHING)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ["name__age_group"]
        constraints = [
            models.UniqueConstraint(
                fields=["group_group_admin_id", "name"],
                name="unique_section_group_group_admin_id_and_name",
            )
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED ScoutsSection")
        return (self.group_group_admin_id,)
