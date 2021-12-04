from django.db import models

from apps.groups.models import ScoutsGroup, ScoutsSectionName


from scouts_auth.inuits.models import AbstractBaseModel


class ScoutsSection(AbstractBaseModel):
    """
    A model for a scouts section, linked to their scouts group and name.
    """

    group = models.ForeignKey(
        ScoutsGroup, related_name="sections", on_delete=models.CASCADE
    )
    name = models.ForeignKey(ScoutsSectionName, on_delete=models.DO_NOTHING)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ["name__age_group"]
