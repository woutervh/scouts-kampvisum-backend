from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel
from ..models import ScoutsGroupType


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

