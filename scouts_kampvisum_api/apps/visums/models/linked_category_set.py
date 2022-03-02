from django.db import models

from apps.camps.models import CampType

from apps.visums.models.enums import CheckState

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategorySet(AbstractBaseModel):

    camp_types = models.ManyToManyField(CampType)

    def is_checked(self) -> CheckState:
        for category in self.categories.all():
            if not category.is_checked():
                return CheckState.UNCHECKED
        return CheckState.CHECKED

    @property
    def readable_name(self):
        return "{} {}".format(
            self.parent.camp_year_category_set.camp_year.year,
            self.parent.camp_type.camp_type,
        )
