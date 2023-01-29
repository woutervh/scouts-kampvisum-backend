from django.db import models

from apps.locations.managers import LinkedLocationManager

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    OptionalEmailField,
    DefaultIntegerField,
)


class LinkedLocation(AuditedBaseModel):

    objects = LinkedLocationManager()

    name = OptionalCharField(max_length=64)
    contact_name = OptionalCharField(max_length=128)
    contact_phone = OptionalCharField(max_length=64)
    contact_email = OptionalEmailField(max_length=128)
    # locations linked through CampLocation object, related_name is 'locations'
    is_camp_location = models.BooleanField(default=False)
    center_latitude = models.FloatField(
        null=True, blank=True, default=50.4956754)
    center_longitude = models.FloatField(
        null=True, blank=True, default=3.3452037)
    zoom = DefaultIntegerField(null=True, blank=True, default=7)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
