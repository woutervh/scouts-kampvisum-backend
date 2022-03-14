from django.db import models

from apps.visums.models import LinkedCategory, SubCategory
from apps.visums.managers import LinkedSubCategoryManager

from scouts_auth.inuits.models import AuditedArchiveableBaseModel


class LinkedSubCategory(AuditedArchiveableBaseModel):

    objects = LinkedSubCategoryManager()

    parent = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    category = models.ForeignKey(
        LinkedCategory, on_delete=models.CASCADE, related_name="sub_categories"
    )

    class Meta:
        ordering = ["parent__index"]

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
