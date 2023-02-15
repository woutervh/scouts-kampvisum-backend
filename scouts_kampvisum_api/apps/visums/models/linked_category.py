from django.db import models

from apps.visums.models import Category, LinkedCategorySet
from apps.visums.models.enums import CheckState
from apps.visums.managers import LinkedCategoryManager

from scouts_auth.inuits.models import AuditedArchiveableBaseModel
from scouts_auth.inuits.models.fields import DefaultCharField


class LinkedCategory(AuditedArchiveableBaseModel):

    objects = LinkedCategoryManager()

    parent = models.ForeignKey(Category, on_delete=models.CASCADE)
    category_set = models.ForeignKey(
        LinkedCategorySet, on_delete=models.CASCADE, related_name="categories"
    )
    check_state = DefaultCharField(
        choices=CheckState.choices,
        default=CheckState.UNCHECKED,
        max_length=32
    )

    class Meta:
        ordering = ["parent__index"]

    def is_checked(self) -> CheckState:
        sub_categories = self.sub_categories.all()
        for sub_category in sub_categories:
            if not sub_category.is_checked():
                return CheckState.UNCHECKED
        return CheckState.CHECKED

    @property
    def readable_name(self):
        return "{}".format(self.parent.name)

    def to_simple_str(self) -> str:
        return "{} ({})".format(self.parent.name, self.id)
