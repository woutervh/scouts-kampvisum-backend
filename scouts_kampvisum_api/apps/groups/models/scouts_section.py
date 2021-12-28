from django.db import models

from apps.groups.models import ScoutsSectionName


from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField


class ScoutsSection(AbstractBaseModel):
    """
    A model for a scouts section, linked to their scouts group and name.
    """

    group_admin_id = RequiredCharField(max_length=64)
    name = models.ForeignKey(ScoutsSectionName, on_delete=models.DO_NOTHING)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ["name__age_group"]
