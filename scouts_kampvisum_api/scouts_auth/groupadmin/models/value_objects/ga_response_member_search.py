from typing import List
from datetime import date

from scouts_auth.groupadmin.models.value_objects import (
    AbstractScoutsResponse,
    AbstractScoutsLink,
)

from scouts_auth.inuits.models import AbstractNonModel, Gender


class AbstractScoutsMemberSearchMember(AbstractNonModel):

    group_admin_id: str
    first_name: str
    last_name: str
    birth_date: date
    email: str
    phone_number: str
    gender: Gender
    inactive_member: bool
    links: List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = "",
        first_name: str = "",
        last_name: str = "",
        birth_date: date = None,
        email: str = "",
        phone_number: str = "",
        inactive_member: bool = False,
        links: List[AbstractScoutsLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.email = email
        self.phone_number = phone_number
        self.inactive_member = inactive_member
        self.links = links if links else []

    def __str__(self):
        return "group_admin_id({}), first_name({}), last_name({}), birth_date({}), email({}), phone_number({}), gender ({}), inactive_member ({}), links({})".format(
            self.group_admin_id,
            self.first_name,
            self.last_name,
            self.birth_date,
            self.email,
            self.phone_number,
            str(self.gender),
            self.inactive_member,
            ", ".join(str(link) for link in self.links) if self.links else "[]",
        )


class AbstractScoutsMemberSearchResponse(AbstractScoutsResponse):
    """Class to capture data returned from a call to /ledenlijst."""

    members: List[AbstractScoutsMemberSearchMember]

    class Meta:
        abstract = True

    def __init__(
        self,
        count: int = 0,
        total: int = 0,
        offset: int = 0,
        filter_criterium: str = "",
        criteria: dict = None,
        members: List[AbstractScoutsMemberSearchMember] = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.members = members if members else []

        super().__init__(count, total, offset, filter_criterium, criteria, links)

    def __str__(self):
        return ("members: ({}), " + super().__str__()).format(
            ", ".join(str(member) for member in self.members) if self.members else "[]"
        )
