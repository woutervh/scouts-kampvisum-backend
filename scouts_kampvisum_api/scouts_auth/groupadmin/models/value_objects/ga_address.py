from django.db import models

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsPosition
from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField


class AbstractScoutsAddress(AbstractNonModel):

    group_admin_id = models.CharField()
    street = OptionalCharField()
    number = OptionalCharField()
    letter_box = OptionalCharField()
    postal_code = OptionalCharField()
    city = OptionalCharField()
    country = OptionalCharField()
    phone_number = OptionalCharField()
    postal_address = models.BooleanField()
    status = OptionalCharField()
    giscode = OptionalCharField()
    description = OptionalCharField()
    # Declare as foreign key in concrete subclasses
    position: AbstractScoutsPosition

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = "",
        street: str = "",
        number: str = "",
        letter_box: str = "",
        postal_code: str = "",
        city: str = "",
        country: str = "",
        phone_number: str = "",
        postal_address: bool = False,
        status: str = "",
        giscode: str = "",
        description: str = "",
        position: AbstractScoutsPosition = None,
    ):
        self.group_admin_id = group_admin_id
        self.street = street
        self.number = number
        self.letter_box = letter_box
        self.postal_code = postal_code
        self.city = city
        self.country = country
        self.phone_number = phone_number
        self.postal_address = postal_address
        self.status = status
        self.giscode = giscode
        self.description = description
        self.position = position

        # super().__init__([], {})

    def __str__(self):
        return "group_admin_id({}), street({}), number({}), letter_box({}), postal_code({}), city({}), country({}), phone_number({}), postal_address({}), status({}), giscode({}), description({}), position({})".format(
            self.group_admin_id,
            self.street,
            self.number,
            self.letter_box,
            self.postal_code,
            self.city,
            self.country,
            self.phone_number,
            self.postal_address,
            self.status,
            self.giscode,
            self.description,
            str(self.position),
        )

    def to_descriptive_string(self):
        return "{} {} {}, {} {}, {}, {}".format(
            self.street, self.number, self.letter_box, self.postal_code, self.city, self.country, self.phone_number
        )
