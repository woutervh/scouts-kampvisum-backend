from django.db import models

from ..models import Concern, LinkedSubCategory
from apps.base.models import BaseModel


class LinkedConcern(BaseModel):

    sub_category = models.ForeignKey(
        LinkedSubCategory, related_name="concerns", on_delete=models.CASCADE
    )
    origin = models.ForeignKey(Concern, on_delete=models.CASCADE)
