import logging

from django.db import models

from apps.visums.managers import CategoryManager
from apps.visums.models import CategorySet

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import (
    RequiredCharField,
    RequiredIntegerField,
    OptionalTextField,
)


logger = logging.getLogger(__name__)


class Category(AbstractBaseModel):

    objects = CategoryManager()

    name = RequiredCharField(max_length=128)
    category_set = models.ForeignKey(
        CategorySet, on_delete=models.CASCADE, related_name="categories"
    )
    index = RequiredIntegerField(default=0)
    description = OptionalTextField()

    class Meta:
        ordering = ["index"]
        unique_together = ("name", "category_set")

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED")
        return (self.name, self.category_set)

    def __str__(self):
        return "OBJECT Category: name({}), category_set({}), index({}), description({})".format(
            self.name, str(self.category_set), self.index, self.description
        )
