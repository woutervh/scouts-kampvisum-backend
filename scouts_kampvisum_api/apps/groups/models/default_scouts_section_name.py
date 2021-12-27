from django.db import models

from apps.groups.models import ScoutsSectionName, ScoutsGroupType

from scouts_auth.inuits.models import AbstractBaseModel


class DefaultScoutsSectionName(AbstractBaseModel):
    """
    A model that configures default section names for a particular group type.

    Currently, if the group is not a zeescouts group, it is assumed the group
    type is 'Groep'.
    """

    type = models.ForeignKey(ScoutsGroupType, null=True, on_delete=models.CASCADE)
    name = models.ForeignKey(ScoutsSectionName, on_delete=models.DO_NOTHING)

    class Meta:
        # Set managed to False unless
        managed = False
        unique_together = ("type", "name")

    def clean(self):
        pass
