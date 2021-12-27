from typing import List

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsLink

from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField


class AbstractScoutsContact(AbstractNonModel):

    member = OptionalCharField()
    function = OptionalCharField()
    name = OptionalCharField()
    phone_number = OptionalCharField()
    email = OptionalCharField()
    links: List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(
        self,
        member: str = "",
        function: str = "",
        name: str = "",
        phone_number: str = "",
        email: str = "",
        links: List[AbstractScoutsLink] = None,
    ):
        self.member = member
        self.function = function
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.links = links if links else []

        # super().__init__([], {})

    def __str__(self):
        return "member({}), function({}), name({}), phone_number({}), email({}), links({})".format(
            self.member,
            self.function,
            self.name,
            self.phone_number,
            self.email,
            ", ".join(str(link) for link in self.links),
        )
