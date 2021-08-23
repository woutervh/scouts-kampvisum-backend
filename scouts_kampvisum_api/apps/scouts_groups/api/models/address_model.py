from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel
from ..models import ScoutsGroup


class ScoutsAddress(BaseModel):
    """
    Contains an address.
    """
    
    group = models.ForeignKey(
        ScoutsGroup,
        related_name='addresses',
        null=True,
        blank=False,
        on_delete=models.CASCADE)
    group_admin_uuid = models.CharField(
        max_length=64, default='', unique=True, null=True, blank=True)
    country = models.CharField(
        max_length=2, default='', null=True, blank=True)
    postal_code = models.CharField(
        max_length=32, default='', null=True, blank=True)
    city = models.CharField(
        max_length=64, default='', null=True, blank=True)
    street = models.CharField(
        max_length=64, default='', null=True, blank=True)
    number = models.CharField(
        max_length=12, default='', null=True, blank=True)
    box = models.CharField(
        max_length=12, default='', null=True, blank=True)
    postal_address = models.BooleanField(default = False)
    status = models.CharField(
        max_length=12, default='', null=True, blank=True)
    latitude = models.CharField(
        max_length=64, default='', null=True, blank=True)
    longitude = models.CharField(
        max_length=64, default='', null=True, blank=True)
    description = models.CharField(
        max_length=128, default='', null=True, blank=True)

