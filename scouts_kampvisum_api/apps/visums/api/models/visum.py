from django.db import models

from ..models import CategorySet
from apps.base.models import BaseModel
from apps.camps.models import Camp


class CampVisum(BaseModel):

    camp = models.ForeignKey(
        Camp, on_delete=models.CASCADE)
    category_set = models.ForeignKey(
<<<<<<< HEAD
        CategorySet, on_delete=models.CASCADE)
=======
        CampVisumCategorySet, on_delete=models.CASCADE)

    class Meta:
        ordering = ["camp__sections__age_group"]
>>>>>>> 84b3060edff6d426426b870a7dd3a2f6f1874391
