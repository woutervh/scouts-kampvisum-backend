from django.db import models

from apps.visums.models import Concern, LinkedSubCategory

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedConcern(AbstractBaseModel):

    # Parent sub-category
    sub_category = models.ForeignKey(
        LinkedSubCategory, related_name="concerns", on_delete=models.CASCADE
    )
    # Reference
    origin = models.ForeignKey(Concern, on_delete=models.CASCADE)
    # Deep copy
    concern = models.ForeignKey(
        Concern, related_name="linked_concern", on_delete=models.CASCADE
    )

    def get_status(self) -> bool:
        pass
