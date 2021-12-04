from django.db import models

from apps.visums.managers import CategoryManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import (
    RequiredCharField,
    RequiredIntegerField,
    OptionalTextField,
)


class Category(AbstractBaseModel):

    name = RequiredCharField(max_length=128)
    index = RequiredIntegerField(default=0)
    description = OptionalTextField()
    is_default = models.BooleanField(default=False)

    objects = CategoryManager()

    class Meta:
        ordering = ["index"]

    def natural_key(self):
        return (self.name,)
