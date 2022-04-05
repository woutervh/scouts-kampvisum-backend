from django.db import models

from apps.visums.models.enums import ApprovalStateEnum

from scouts_auth.inuits.models.fields import DefaultCharField


class CampVisumApprovalMixin(models.model):

    approval = DefaultCharField(
        choices=ApprovalStateEnum.choices,
        default=ApprovalStateEnum.DEADLINE,
        max_length=1,
    )

    class Meta:
        abstract = True
        permissions = [
            ("view_visum_approval", "User is a DC and can view approval status"),
            ("edit_visum_approval", "User is a DC and can set approval status"),
        ]
