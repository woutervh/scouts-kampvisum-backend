from django.db import models

from apps.visums.models import LinkedCategory, SubCategory
from apps.visums.models.enums import CheckState
from apps.visums.managers import LinkedSubCategoryManager

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedSubCategory(AbstractBaseModel):
    
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
