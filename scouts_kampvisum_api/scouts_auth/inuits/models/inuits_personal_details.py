from django.db import models

from scouts_auth.inuits.models import Gender
from scouts_auth.inuits.models.fields import OptionalCharField, DefaultCharField, OptionalEmailField, OptionalDateField


class InuitsPersonalDetails(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    phone_number = OptionalCharField(max_length=24)
    cell_number = OptionalCharField(max_length=24)
    email = OptionalEmailField()
    birth_date = OptionalDateField()
    gender = DefaultCharField(choices=Gender.choices, default=Gender.UNKNOWN, max_length=1)

    class Meta:
        abstract = True
