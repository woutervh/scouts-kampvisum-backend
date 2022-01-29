from django.db import models

from scouts_auth.inuits.models.fields import OptionalTextField
from scouts_auth.inuits.utils import TextUtils


class Explainable(models.Model):
    """Provides a translatable explanation for an object (field name: explanation)"""

    explanation = OptionalTextField()

    class Meta:
        abstract = True

    def has_explanation(self) -> bool:
        return TextUtils.is_non_empty(self.explanation)
