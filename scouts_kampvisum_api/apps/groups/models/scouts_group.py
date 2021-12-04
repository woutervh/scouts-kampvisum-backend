from django.db import models

from apps.groups.models import ScoutsGroupType

from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_auth.inuits.models import AuditedBaseModel


class ScoutsGroup(AbstractScoutsGroup, AuditedBaseModel):
    """
    A scouts group.
    """

    type = models.ForeignKey(
        ScoutsGroupType,
        related_name="group_type",
        null=True,
        blank=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["group_admin_id", "number"]
