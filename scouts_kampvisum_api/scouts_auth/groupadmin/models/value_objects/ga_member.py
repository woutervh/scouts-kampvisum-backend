from typing import List
import datetime

from django.db import models


from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
from scouts_auth.groupadmin.models.value_objects import (
    AbstractScoutsAddress,
    AbstractScoutsContact,
    AbstractScoutsFunction,
    AbstractScoutsLink,
    AbstractScoutsGroup,
    AbstractScoutsGroupSpecificField,
    AbstractScoutsMemberSearchMember,
)

from scouts_auth.inuits.models import AbstractNonModel, Gender, GenderHelper
from scouts_auth.inuits.models.fields import OptionalCharField, OptionalDateField


class AbstractScoutsMemberPersonalData(AbstractNonModel):

    phone_number = OptionalCharField()
    gender: Gender = models.CharField(
        choices=Gender, default=Gender.UNKNOWN, max_length="1"
    )

    class Meta:
        abstract = True

    def __init__(self, gender: Gender = None, phone_number: str = ""):
        self.gender = (
            gender
            if gender and isinstance(gender, Gender)
            else GenderHelper.parse_gender(gender)
        )
        self.phone_number = phone_number

    def has_gender(self):
        return self.gender and GenderHelper.parse_gender(self.gender) != Gender.UNKNOWN

    def __str__(self):
        return "gender({}), phone_number({})".format(self.gender, self.phone_number)


class AbstractScoutsMemberGroupAdminData(AbstractNonModel):

    first_name = OptionalCharField()
    last_name = OptionalCharField()
    birth_date = OptionalDateField()

    class Meta:
        abstract = True

    def __init__(
        self,
        first_name: str = "",
        last_name: str = "",
        birth_date: datetime.date = None,
    ):
        self.first_name = first_name
        self.last_name = last_name

        if isinstance(birth_date, datetime.date):
            self.birth_date = birth_date
        if isinstance(birth_date, str):
            self.birth_date = datetime.datetime.strptime(
                birth_date, "%Y-%m-%d").date()

        # super().__init__([], {})

    def __str__(self):
        return "first_name({}), last_name({}), birth_date({})".format(
            self.first_name, self.last_name, self.birth_date
        )


class AbstractScoutsMemberScoutsData(AbstractNonModel):

    membership_number = OptionalCharField()
    customer_number = OptionalCharField()

    class Meta:
        abstract = True

    def __init__(self, membership_number: str = "", customer_number: str = ""):
        self.membership_number = membership_number
        self.customer_number = customer_number

        # super().__init__([], {})

    def __str__(self):
        return "membership_number({}), customer_number({})".format(
            self.customer_number, self.membership_number
        )


class AbstractScoutsMember(AbstractNonModel):

    personal_data: AbstractScoutsMemberPersonalData
    group_admin_data: AbstractScoutsMemberGroupAdminData
    scouts_data: AbstractScoutsMemberScoutsData
    email: str
    username: str
    group_admin_id = OptionalGroupAdminIdField()
    _inactive_member: bool = False
    addresses: List[AbstractScoutsAddress]
    contacts: List[AbstractScoutsContact]
    functions: List[AbstractScoutsFunction]
    scouts_groups: List[AbstractScoutsGroup]
    group_specific_fields: List[AbstractScoutsGroupSpecificField]
    links: List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(
        self,
        personal_data: AbstractScoutsMemberPersonalData = None,
        group_admin_data: AbstractScoutsMemberGroupAdminData = None,
        scouts_data: AbstractScoutsMemberScoutsData = None,
        email: str = "",
        username: str = "",
        group_admin_id: str = "",
        inactive_member: bool = False,
        addresses: List[AbstractScoutsAddress] = None,
        contacts: List[AbstractScoutsContact] = None,
        functions: List[AbstractScoutsFunction] = None,
        scouts_groups: List[AbstractScoutsGroup] = None,
        group_specific_fields: List[AbstractScoutsGroupSpecificField] = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.personal_data = (
            personal_data if personal_data else AbstractScoutsMemberPersonalData()
        )
        self.group_admin_data = (
            group_admin_data
            if group_admin_data
            else AbstractScoutsMemberGroupAdminData()
        )
        self.scouts_data = (
            scouts_data if scouts_data else AbstractScoutsMemberScoutsData()
        )
        self.email = email
        self.username = username
        self.group_admin_id = group_admin_id
        self._inactive_member = inactive_member
        self.addresses = addresses if addresses else []
        self.contacts = contacts if contacts else []
        self.functions = functions if functions else []
        self.scouts_groups = scouts_groups if scouts_groups else []
        self.group_specific_fields = (
            group_specific_fields if group_specific_fields else []
        )
        self.links = links if links else []

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    def get_function_codes(self) -> List[str]:
        return [function.code for function in self.functions]

    @property
    def gender(self):
        return self.personal_data.gender

    def has_gender(self):
        return self.personal_data.has_gender()

    @property
    def phone_number(self):
        return self.personal_data.phone_number

    @property
    def cell_number(self):
        return self.phone_number

    @property
    def first_name(self):
        return self.group_admin_data.first_name

    @first_name.setter
    def first_name(self, first_name: str):
        self.group_admin_data.first_name = first_name

    @property
    def last_name(self):
        return self.group_admin_data.last_name

    @last_name.setter
    def last_name(self, last_name: str):
        self.group_admin_data.last_name = last_name

    @property
    def birth_date(self):
        return self.group_admin_data.birth_date

    @birth_date.setter
    def birth_date(self, birth_date):
        if isinstance(birth_date, datetime.datetime):
            birth_date = birth_date.date()
        self.group_admin_data.birth_date = birth_date

    @property
    def membership_number(self):
        return self.scouts_data.membership_number

    @property
    def customer_number(self):
        return self.scouts_data.customer_number

    @property
    def address(self):
        if len(self.addresses) > 0:
            return self.addresses[0]
        return AbstractScoutsAddress()

    @property
    def street(self):
        return self.address.street

    @property
    def number(self):
        return self.address.number

    @property
    def letter_box(self):
        return self.address.letter_box

    @property
    def postal_code(self):
        return self.address.postal_code

    @property
    def city(self):
        return self.address.city

    @property
    def inactive_member(self):
        return self._inactive_member

    @inactive_member.setter
    def inactive_member(self, value: bool):
        self._inactive_member = value

    def __str__(self):
        return (
            self.personal_data.__str__()
            + ", "
            + self.group_admin_data.__str__()
            + ", "
            + self.scouts_data.__str__()
            + ", email({}), username({}), group_admin_id({}), inactive_member ({}), addresses({}), contacts({}), functions({}), groups({}), group_specific_fields ({}), links({})"
        ).format(
            self.email,
            self.username,
            self.group_admin_id,
            self.inactive_member,
            ", ".join(str(address) for address in self.addresses)
            if self.addresses
            else "[]",
            ", ".join(str(contact) for contact in self.contacts)
            if self.contacts
            else "[]",
            ", ".join(str(function) for function in self.functions)
            if self.functions
            else "[]",
            ", ".join(str(group) for group in self.scouts_groups)
            if self.scouts_groups
            else "[]",
            ", ".join(str(field) for field in self.group_specific_fields)
            if self.group_specific_fields
            else "[]",
            ", ".join(str(link)
                      for link in self.links) if self.links else "[]",
        )

    def to_search_member(self) -> AbstractScoutsMemberSearchMember:
        member = AbstractScoutsMemberSearchMember(
            group_admin_id=self.group_admin_id,
            inactive_member=self.inactive_member,
            first_name=self.group_admin_data.first_name,
            last_name=self.group_admin_data.last_name,
            birth_date=self.group_admin_data.birth_date,
            email=self.email,
            phone_number=self.personal_data.phone_number,
            links=self.links,
        )

        member.gender = self.gender

        return member
