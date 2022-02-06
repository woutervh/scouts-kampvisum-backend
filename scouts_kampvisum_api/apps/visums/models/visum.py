from django.db import models

from apps.camps.models import Camp

from apps.visums.models import LinkedCategorySet
from apps.visums.managers import CampVisumManager

from scouts_auth.inuits.models import AbstractBaseModel


class CampVisum(AbstractBaseModel):
    
    objects = CampVisumManager()

    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    category_set = models.ForeignKey(
        LinkedCategorySet, on_delete=models.CASCADE, related_name="visum"
    )

    class Meta:
        # ordering = ["camp__sections__name__age_group"]
        pass
