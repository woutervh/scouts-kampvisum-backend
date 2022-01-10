from django.db import models

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField


class Location(AbstractBaseModel):

    name = OptionalCharField(max_length=64)
    address = OptionalCharField(max_length=254)
    is_main_location = models.BooleanField(default=False)
