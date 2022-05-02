from django.db import models

from apps.visums.models import LinkedCategory, SubCategory
from apps.visums.models.enums import CampVisumApprovalState
from apps.visums.managers import LinkedSubCategoryManager

from scouts_auth.inuits.models import AuditedArchiveableBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField, DefaultCharField


class LinkedSubCategory(AuditedArchiveableBaseModel):

    objects = LinkedSubCategoryManager()

    parent = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    category = models.ForeignKey(
        LinkedCategory, on_delete=models.CASCADE, related_name="sub_categories"
    )

    feedback = OptionalCharField(max_length=300)
    approval = DefaultCharField(
        choices=CampVisumApprovalState.choices,
        default=CampVisumApprovalState.UNDECIDED,
        max_length=1,
    )

    class Meta:
        ordering = ["parent__index"]
        permissions = [
            ("view_visum_feedback", "User can view the DC's feedback"),
            ("edit_visum_feedback", "User is a DC and can edit the feedback"),
            ("view_visum_approval", "User can view approval status"),
            ("edit_visum_approval", "User is a DC and can set approval status"),
        ]

    # def is_checked(self) -> CheckState:
    #     for check in self.checks.all():
    #         if not check.is_checked():
    #             return CheckState.UNCHECKED
    #     return CheckState.CHECKED

    @property
    def readable_name(self):
        return "{}".format(self.parent.name)

    def is_checked(self) -> bool:
        for check in self.checks.all():
            if not check.get_value_type().is_checked():
                return False

        return True

    def to_simple_str(self) -> str:
        return "{} ({})".format(self.parent.name, self.id)
