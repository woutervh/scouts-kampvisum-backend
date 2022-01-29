from django.db import models

from scouts_auth.inuits.models.fields import OptionalTextField
from scouts_auth.inuits.utils import TextUtils


class Describable(models.Model):
    """Provides a translatable description for an object (field name: description)"""

    description = OptionalTextField()

    class Meta:
        abstract = True

    def has_description(self) -> bool:
        return TextUtils.is_non_empty(self.description)
