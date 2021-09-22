from django.db import models

from apps.base.models import BaseModel
from ..managers import CategoryManager
from inuits.models import (
    RequiredCharField,
    RequiredIntegerField,
    OptionalTextField,
)


class Category(BaseModel):

    name = RequiredCharField(max_length=128)
    index = RequiredIntegerField(default=0)
    description = OptionalTextField()
    is_default = models.BooleanField(default=False)

    objects = CategoryManager()

    class Meta:
        ordering = ["index"]

    def natural_key(self):
        return (self.name,)
