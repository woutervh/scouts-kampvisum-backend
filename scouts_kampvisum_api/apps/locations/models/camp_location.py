from django.db import models

from apps.visums.models import LinkedLocationCheck
from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField


class CampLocation(AbstractBaseModel):

    location_check = models.ForeignKey(
        LinkedLocationCheck, on_delete=models.CASCADE, related_name="locations"
    )
    name = OptionalCharField(max_length=64)
    address = OptionalCharField(max_length=254)
    is_main_location = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
