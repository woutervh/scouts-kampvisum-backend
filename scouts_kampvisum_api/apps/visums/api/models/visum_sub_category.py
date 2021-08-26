from django.db import models

from ..models import CampVisumCategory
from apps.base.models import BaseModel
from apps.camps.models import Camp
from inuits.models import OptionalTextField


class CampVisumLinkedSubCategory(BaseModel):

    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    category = models.ForeignKey(CampVisumCategory, on_delete=models.CASCADE)
    description = OptionalTextField()
    comments = OptionalTextField()

    def get_status(self):
        checks = self.checks
