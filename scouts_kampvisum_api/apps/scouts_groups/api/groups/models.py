from django.db import models
from django.utils import timezone

from ....base.models import BaseModel
from .managers import ScoutsGroupTypeManager


class ScoutsGroupType(BaseModel):
    """
    Specifies the type of scouts group (e.g. AKABE, zeescouts, ...).
    """
    
    type = models.CharField(
        max_length=64,
        null=False,
        blank=False)

    objects = ScoutsGroupTypeManager()
    
    class Meta:
        abstract = False
        ordering = ['type']
    
    def natural_key(self):
        return (self.type, )
    
    def clean(self):
        pass


class ScoutsGroup(BaseModel):
    """
    A ScoutsGroup.
    """
    
    group_admin_id = models.CharField(
        max_length=32, default='', unique=True, null=True, blank=True)
    number = models.CharField(
        max_length=32, default='', null=True, blank=True)
    name = models.CharField(
        max_length=32, default='', null=True, blank=True)
    foundation = models.DateTimeField(
        default=timezone.now, null=True, blank=True)
    only_leaders = models.BooleanField(default=False)
    show_members_improved = models.BooleanField(default=False)
    email = models.CharField(
        max_length=128, default='', null=True, blank=True)
    website = models.CharField(
        max_length=128, default='', null=True, blank=True)
    info = models.CharField(
        max_length=128, default='', null=True, blank=True)
    sub_groups = models.ForeignKey(
        'ScoutsGroup',
        related_name='%(class)s_sub_groups',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        ScoutsGroupType,
        related_name='group_type',
        null=True,
        blank=False,
        on_delete=models.CASCADE)
    public_registration = models.BooleanField(default=False)

    class Meta:
        ordering = ['group_admin_id', 'number']
    
    def clean(self):
        pass


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

