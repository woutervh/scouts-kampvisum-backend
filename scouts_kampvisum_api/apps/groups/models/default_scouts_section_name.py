from django.db import models
from django.core.exceptions import ValidationError

from apps.groups.managers import DefaultScoutsSectionNameManager
from apps.groups.models import ScoutsGroupType

from scouts_auth.inuits.models import AbstractBaseModel, Gender
from scouts_auth.inuits.models.fields import (
    RequiredCharField,
    DefaultCharField,
    DefaultIntegerField,
)


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
    name = RequiredCharField(max_length=128)
    gender = DefaultCharField(
        choices=Gender.choices,
        default=Gender.UNKNOWN,
        max_length=1,
    )
    age_group = DefaultIntegerField(default=0)
    hidden = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group_type", "name", "gender", "age_group"],
                name="unique_group_type_and_name_gender_age_group_for_default_scouts_section_name",
            )
        ]

    def clean(self):
        if self.group_type is None or self.name is None:
            raise ValidationError(
                "A DefaultScoutsSectionName needs a group type and a section name"
            )

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED DefaultScoutsSectionName")
        return (self.group_type, self.name, self.gender, self.age_group)
