from django.db import models

from scouts_auth.inuits.models.fields import OptionalCharField, OptionalIntegerField


class InuitsAddress(models.Model):
    street = OptionalCharField(max_length=100)
    number = OptionalCharField(max_length=5)
    letter_box = OptionalCharField(max_length=5)
    postal_code = OptionalIntegerField()
    city = OptionalCharField(max_length=40)
    # country = models.ForeignKey(InuitsCountry, on_delete=models.CASCADE, null=True, related_name="address")

    class Meta:
        abstract = True
