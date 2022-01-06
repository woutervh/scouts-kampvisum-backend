from django.db import models

from apps.visums.models import LinkedSubCategory, Check

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCheck(AbstractBaseModel):

    parent = models.ForeignKey(Check, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        LinkedSubCategory, on_delete=models.CASCADE, related_name="checks"
    )
