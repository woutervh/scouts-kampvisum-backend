from django.db import models

from apps.visums.models import SubCategory, ConcernType

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import Translatable, Linkable, Explainable


class Concern(Translatable, Linkable, Explainable, AbstractBaseModel):

    name = RequiredCharField(max_length=64)
    sub_category = models.ForeignKey(
        SubCategory, related_name="concerns", on_delete=models.CASCADE
    )
    type = models.ForeignKey(ConcernType, on_delete=models.CASCADE)
    is_default = False

    class Meta:
        ordering = ["name"]
