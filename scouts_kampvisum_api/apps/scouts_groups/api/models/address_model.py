from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel
from ..models import ScoutsGroup
from inuits.models import OptionalCharField


class ScoutsAddress(BaseModel):
    """
    Contains an address.
    """
    
    group = models.ForeignKey(
        ScoutsGroup,
        related_name='addresses',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    group_admin_uuid = OptionalCharField(max_length=64, unique=True)
    country = OptionalCharField(max_length=2)
    postal_code = OptionalCharField(max_length=32)
    city = OptionalCharField(max_length=64)
    street = OptionalCharField(max_length=64)
    number = OptionalCharField(max_length=12)
    box = OptionalCharField(max_length=12)
    postal_address = models.BooleanField(default = False)
    status = OptionalCharField(max_length=12)
    latitude = OptionalCharField(max_length=64)
    longitude = OptionalCharField(max_length=64)
    description = OptionalCharField(max_length=128)

