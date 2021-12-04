from django.db import models

from apps.groups.models import ScoutsGroup

from scouts_auth.groupadmin.models import AbstractScoutsAddress
from scouts_auth.inuits.models import AbstractBaseModel


class ScoutsAddress(AbstractScoutsAddress, AbstractBaseModel):
    """
    Contains an address.
    """

    group = models.ForeignKey(
        ScoutsGroup,
        related_name="addresses",
        null=True,
        blank=False,
        on_delete=models.CASCADE,
    )
