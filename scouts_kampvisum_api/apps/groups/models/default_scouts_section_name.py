from django.db import models
from django.core.exceptions import ValidationError

from apps.groups.managers import DefaultScoutsSectionNameManager
from apps.groups.models import ScoutsSectionName, ScoutsGroupType

from scouts_auth.inuits.models import AbstractBaseModel


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultScoutsSectionName(AbstractBaseModel):
    """
    A model that configures default section names for a particular group type.

    Currently, if the group is not a zeescouts group, it is assumed the group
    type is 'Groep'.
    """

    objects = DefaultScoutsSectionNameManager()

    group_type = models.ForeignKey(ScoutsGroupType, null=True, on_delete=models.CASCADE)
    name = models.ForeignKey(ScoutsSectionName, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group_type", "name"],
                name="unique_group_type_and_name_for_default_scouts_section_name",
            )
        ]

    def clean(self):
        if self.group_type is None or self.name is None:
            raise ValidationError(
                "A DefaultScoutsSectionName needs a group type and a section name"
            )

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED DefaultScoutsSectionName")
        return (self.group_type, self.name)
