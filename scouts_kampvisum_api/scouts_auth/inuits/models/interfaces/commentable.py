from django.db import models

from scouts_auth.inuits.models.fields import OptionalTextField
from scouts_auth.inuits.utils import TextUtils


class Commentable(models.Model):

    comment = OptionalTextField()

    class Meta:
        abstract = True

    def has_comment(self) -> bool:
        return TextUtils.is_non_empty(self.comment)
