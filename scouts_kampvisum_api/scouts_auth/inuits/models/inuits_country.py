from django.db import models

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField
from scouts_auth.inuits.managers import InuitsCountryManager


class InuitsCountry(models.Model):

    # objects = InuitsCountryManager()

    name = models.CharField(max_length=64)
    code = OptionalCharField(max_length=2)

    class Meta:
        abstract = True

    # def natural_key(self):
    #     return (self.code,)
    def natural_key(self):
        return self.name
