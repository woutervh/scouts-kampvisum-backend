import logging

from django.db import models
from django.core.exceptions import ValidationError

from apps.groups.managers import DefaultScoutsSectionNameManager
from apps.groups.models import ScoutsSectionName, ScoutsGroupType

from scouts_auth.inuits.models import AbstractBaseModel


logger = logging.getLogger(__name__)


class DefaultScoutsSectionName(AbstractBaseModel):
    """
    A model that configures default section names for a particular group type.

    Currently, if the group is not a zeescouts group, it is assumed the group
    type is 'Groep'.
    """

    objects = DefaultScoutsSectionNameManager()

    type = models.ForeignKey(ScoutsGroupType, null=True, on_delete=models.CASCADE)
    name = models.ForeignKey(ScoutsSectionName, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("type", "name")

    def clean(self):
        if self.type is None or self.name is None:
            raise ValidationError(
                "A DefaultScoutsSectionName needs a group type and a section name"
            )

    def natural_key(self):
        return (self.type, self.name)
