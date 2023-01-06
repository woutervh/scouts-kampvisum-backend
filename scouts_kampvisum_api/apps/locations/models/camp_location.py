from django.db import models

from apps.locations.models import LinkedLocation
from apps.locations.managers import CampLocationManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField


class CampLocation(AbstractBaseModel):

    objects = CampLocationManager()

    location = models.ForeignKey(
        LinkedLocation, on_delete=models.CASCADE, related_name="locations"
    )
    name = OptionalCharField(max_length=64)
    address = OptionalCharField(max_length=254)
    is_main_location = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    country = OptionalCharField(max_length=254)
    postalcode = OptionalCharField(max_length=254)
    township = OptionalCharField(max_length=254)
    street = OptionalCharField(max_length=254)
    house_number = OptionalCharField(max_length=254)
