from django.db import models

from apps.visums.models import CategorySet
from apps.visums.models.enums import CheckState

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategorySet(AbstractBaseModel):

    parent = models.ForeignKey(CategorySet, on_delete=models.CASCADE)
    
    def is_checked(self) -> CheckState:
        for category in self.categories.all():
            if not category.is_checked():
                return CheckState.UNCHECKED
        return CheckState.CHECKED
