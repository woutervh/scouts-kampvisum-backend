from apps.people.models import Person

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField


class ContactPerson(Person, AbstractBaseModel):

    name = OptionalCharField(max_length=128)
    phone = OptionalCharField(max_length=64)
