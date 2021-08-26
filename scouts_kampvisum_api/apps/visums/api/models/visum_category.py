from django.db import models

from ..models import CampVisumCategory
from apps.base.models import BaseModel
from apps.camps.models import Camp

class CampVisumLinkedCategory(BaseModel):

    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    category = models.ForeignKey(
        CampVisumCategory, on_delete=models.CASCADE)

