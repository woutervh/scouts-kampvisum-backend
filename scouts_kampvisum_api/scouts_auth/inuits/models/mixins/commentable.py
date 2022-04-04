from django.db import models

from scouts_auth.inuits.models.fields import OptionalTextField
from scouts_auth.inuits.utils import TextUtils


class Commentable(models.Model):
    """Provides a translatable comment for an object (field name: comment)"""

    comment = OptionalTextField()

    class Meta:
        abstract = True

    def has_comment(self) -> bool:
        return TextUtils.is_non_empty(self.comment)
