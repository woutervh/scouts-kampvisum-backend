from typing import List
from datetime import date

from scouts_auth.groupadmin.models.value_objects import (
    AbstractScoutsAddress,
    AbstractScoutsContact,
    AbstractScoutsLink,
    AbstractScoutsGroupSpecificField,
)


class AbstractScoutsGroup:
    """Models the scouts groups a user has rights to."""

    group_admin_id: str
    number: str
    name: str
    date_of_foundation: date
    bank_account: str
    email: str
    website: str
    info: str
    type: str
    only_leaders: bool
    show_members_improved: bool
    addresses: List[AbstractScoutsAddress]
    contacts: List[AbstractScoutsContact]
    group_specific_fields: List[AbstractScoutsGroupSpecificField]
    links: List[AbstractScoutsLink]

    def __init__(
        self,
        group_admin_id: str = "",
        number: str = "",
        name: str = "",
        date_of_foundation: date = None,
        bank_account: str = "",
        email: str = "",
        website: str = "",
        info: str = "",
        type: str = "",
        only_leaders: bool = False,
        show_members_improved: bool = False,
        addresses: List[AbstractScoutsAddress] = None,
        contacts: List[AbstractScoutsContact] = None,
        group_specific_fields: List[AbstractScoutsGroupSpecificField] = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.number = number
        self.name = name
        self.date_of_foundation = date_of_foundation
        self.bank_account = bank_account
        self.email = email
        self.website = website
        self.info = info
        self.type = type
        self.only_leaders = only_leaders
        self.show_members_improved = show_members_improved
        self.addresses = addresses if addresses else []
        self.contacts = contacts if contacts else []
        self.group_specific_fields = group_specific_fields if group_specific_fields else []
        self.links = links if links else []

    def __str__(self):
        return "group_admin_id({}), number({}), name({}), addresses({}), date_of_foundation({}), only_leaders({}), show_member_improved({}), bank_account({}), email({}), website({}), info({}), type({}), contacts({}), group_specific_fields ({}), links({})".format(
            self.group_admin_id,
            self.number,
            self.name,
            ", ".join(str(address) for address in self.addresses),
            self.date_of_foundation,
            self.only_leaders,
            self.show_members_improved,
            self.bank_account,
            self.email,
            self.website,
            self.info,
            self.type,
            ", ".join(str(contact) for contact in self.contacts),
            ", ".join(str(field) for field in self.group_specific_fields),
            ", ".join(str(link) for link in self.links),
        )

    def to_simple_string(self) -> str:
        return "group_admin_id({}), name({})".format(self.group_admin_id, self.name)
