from django.db import models

from ..models import CampVisumConcern, CampVisumConcernType
from apps.base.models import BaseModel
from apps.camps.models import Camp


class CampVisumLinkedConcern(BaseModel):

    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    concern = models.ForeignKey(CampVisumConcern, on_delete=models.CASCADE)
    type = models.ForeignKey(CampVisumConcernType, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
