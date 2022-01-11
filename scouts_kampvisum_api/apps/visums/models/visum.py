from django.db import models

from apps.visums.models import LinkedCategorySet
from apps.camps.models import Camp

from scouts_auth.inuits.models import AbstractBaseModel


class CampVisum(AbstractBaseModel):

    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    category_set = models.ForeignKey(LinkedCategorySet, on_delete=models.CASCADE)

    class Meta:
        # ordering = ["camp__sections__name__age_group"]
        pass
