from typing import List
from datetime import date

from scouts_auth.groupadmin.models.value_objects import (
    AbstractScoutsAddress,
    AbstractScoutsContact,
    AbstractScoutsFunction,
    AbstractScoutsLink,
    AbstractScoutsGroup,
    AbstractScoutsGroupSpecificField,
    AbstractAbstractScoutsMemberSearchMember,
)

from scouts_auth.inuits.models import Gender, GenderHelper


class AbstractAbstractScoutsMemberPersonalData:

    gender: Gender
    phone_number: str

    def __init__(self, gender: Gender = None, phone_number: str = ""):
        self.gender = gender if gender and isinstance(gender, Gender) else GenderHelper.parse_gender(gender)
        self.phone_number = phone_number

    def __str__(self):
        return "gender({}), phone_number({})".format(self.gender, self.phone_number)


class AbstractAbstractScoutsMemberGroupAdminData:

    first_name: str
    last_name: str
    birth_date: date

    def __init__(self, first_name: str = "", last_name: str = "", birth_date: date = None):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def __str__(self):
        return "first_name({}), last_name({}), birth_date({})".format(self.first_name, self.last_name, self.birth_date)


class AbstractAbstractScoutsMemberScoutsData:

    membership_number: str
    customer_number: str

    def __init__(self, membership_number: str = "", customer_number: str = ""):
        self.membership_number = membership_number
        self.customer_number = customer_number

    def __str__(self):
        return "membership_number({}), customer_number({})".format(self.customer_number, self.membership_number)


class AbstractScoutsMember:

    personal_data: AbstractAbstractScoutsMemberPersonalData
    group_admin_data: AbstractAbstractScoutsMemberGroupAdminData
    scouts_data: AbstractAbstractScoutsMemberScoutsData
    email: str
    username: str
    group_admin_id: str
    addresses: List[AbstractScoutsAddress]
    contacts: List[AbstractScoutsContact]
    functions: List[AbstractScoutsFunction]
    scouts_groups: List[AbstractScoutsGroup]
    group_specific_fields: List[AbstractScoutsGroupSpecificField]
    links: List[AbstractScoutsLink]

    def __init__(
        self,
        personal_data: AbstractAbstractScoutsMemberPersonalData = None,
        group_admin_data: AbstractAbstractScoutsMemberGroupAdminData = None,
        scouts_data: AbstractAbstractScoutsMemberScoutsData = None,
        email: str = "",
        username: str = "",
        group_admin_id: str = "",
        addresses: List[AbstractScoutsAddress] = None,
        contacts: List[AbstractScoutsContact] = None,
        functions: List[AbstractScoutsFunction] = None,
        scouts_groups: List[AbstractScoutsGroup] = None,
        group_specific_fields: List[AbstractScoutsGroupSpecificField] = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.personal_data = personal_data
        self.group_admin_data = group_admin_data
        self.scouts_data = scouts_data
        self.email = email
        self.username = username
        self.group_admin_id = group_admin_id
        self.addresses = addresses if addresses else []
        self.contacts = contacts if contacts else []
        self.functions = functions if functions else []
        self.scouts_groups = scouts_groups if scouts_groups else []
        self.group_specific_fields = group_specific_fields if group_specific_fields else []
        self.links = links if links else []

    def get_function_codes(self) -> List[str]:
        return [function.code for function in self.functions]

    @property
    def gender(self):
        return self.personal_data.gender

    @property
    def phone_number(self):
        return self.personal_data.phone_number

    @property
    def first_name(self):
        return self.group_admin_data.first_name

    @property
    def last_name(self):
        return self.group_admin_data.last_name

    @property
    def birth_date(self):
        return self.group_admin_data.birth_date

    @property
    def membership_number(self):
        return self.scouts_data.membership_number

    @property
    def customer_number(self):
        return self.scouts_data.customer_number

    def __str__(self):
        return (
            self.personal_data.__str__()
            + ", "
            + self.group_admin_data.__str__()
            + ", "
            + self.scouts_data.__str__()
            + ", email({}), username({}), group_admin_id({}), addresses({}), contacts({}), functions({}), groups({}), group_specific_fields ({}), links({})"
        ).format(
            self.email,
            self.username,
            self.group_admin_id,
            ", ".join(str(address) for address in self.addresses),
            ", ".join(str(contact) for contact in self.contacts),
            ", ".join(str(function) for function in self.functions),
            ", ".join(str(group) for group in self.scouts_groups),
            ", ".join(str(field) for field in self.group_specific_fields),
            ", ".join(str(link) for link in self.links),
        )

    def to_search_member(self) -> AbstractAbstractScoutsMemberSearchMember:
        member = AbstractAbstractScoutsMemberSearchMember(
            group_admin_id=self.group_admin_id,
            first_name=self.group_admin_data.first_name,
            last_name=self.group_admin_data.last_name,
            birth_date=self.group_admin_data.birth_date,
            email=self.email,
            phone_number=self.personal_data.phone_number,
            links=self.links,
        )

        member.gender = self.get_gender()

        return member
