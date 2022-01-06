from django.db import models

from apps.visums.models import CategorySet

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategorySet(AbstractBaseModel):

    parent = models.ForeignKey(CategorySet, on_delete=models.CASCADE)
