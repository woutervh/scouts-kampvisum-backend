from django.db import models

from apps.visums.models import CampVisum
from apps.visums.models.enums import CheckState

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategorySet(AbstractBaseModel):

    visum = models.OneToOneField(
        CampVisum, on_delete=models.CASCADE, related_name="category_set"
    )

    def is_checked(self) -> CheckState:
        categories = self.categories.all()
        for category in categories:
            if not category.is_checked():
                return CheckState.UNCHECKED
        return CheckState.CHECKED

    @property
    def readable_name(self):
        return "{} {}".format(
            self.visum.year.year,
            ",".join(
                camp_type.camp_type for camp_type in self.visum.camp_types.all()),
        )
