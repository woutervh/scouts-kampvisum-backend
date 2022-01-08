import logging

from django.db import models

from apps.visums.models import Category
from apps.visums.managers import SubCategoryManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import (
    Describable,
    Explainable,
    Indexable,
    Linkable,
)


logger = logging.getLogger(__name__)


class SubCategory(Describable, Explainable, Indexable, Linkable, AbstractBaseModel):

    objects = SubCategoryManager()

    category = models.ForeignKey(
        Category,
        related_name="sub_categories",
        on_delete=models.CASCADE,
    )
    name = RequiredCharField(max_length=128)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "category")

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED")
        return (self.name, self.category)

    def __str__(self):
        return "OBJECT SubCategory: name({}), category({})".format(
            self.name, str(self.category)
        )
