from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel
from ..models import ScoutsGroupType
from inuits.models import OptionalCharField, OptionalDateField


class ScoutsGroup(BaseModel):
    """
    A ScoutsGroup.
    """
    
    group_admin_id = OptionalCharField(max_length=32, unique=True)
    number = OptionalCharField(max_length=32)
    name = OptionalCharField(max_length=32)
    foundation = OptionalDateField()
    only_leaders = models.BooleanField(default=False)
    show_members_improved = models.BooleanField(default=False)
    email = OptionalCharField(max_length=128)
    website = OptionalCharField(max_length=128)
    info = OptionalCharField(max_length=128)
    # sub_groups = models.ForeignKey(
    #     'ScoutsGroup',
    #     related_name='%(class)s_sub_groups',
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE
    # )
    type = models.ForeignKey(
        ScoutsGroupType,
        related_name='group_type',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    public_registration = models.BooleanField(default=False)

    class Meta:
        ordering = ['group_admin_id', 'number']

