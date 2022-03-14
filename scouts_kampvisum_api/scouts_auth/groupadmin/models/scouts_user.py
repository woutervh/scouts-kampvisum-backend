from typing import List, Tuple
from datetime import date, datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import UserManager

from scouts_auth.auth.models import User

from scouts_auth.groupadmin.models import (
    AbstractScoutsAddress,
    AbstractScoutsFunction,
    AbstractScoutsGroupSpecificField,
    AbstractScoutsLink,
    AbstractScoutsGroup,
    ScoutsGroup,
    ScoutsFunction,
)
from scouts_auth.groupadmin.settings import GroupadminSettings

from scouts_auth.inuits.models import Gender
from scouts_auth.inuits.models.fields import TimezoneAwareDateTimeField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserManager(UserManager):
    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        username = kwargs.get("username", None)
        group_admin_id = kwargs.get("group_admin_id", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if username:
            try:
                return self.get_by_natural_key(username)
            except:
                pass

        if group_admin_id:
            try:
                return self.get_queryset().get(group_admin_id=group_admin_id)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsGroup instance(s) with the provided params: (id: {}, group_admin_id: {})".format(
                    pk,
                    group_admin_id,
                )
            )
        return None

    def get_by_natural_key(self, username):
        logger.trace(
            "GET BY NATURAL KEY %s: (username: %s (%s))",
            "ScoutsUser",
            username,
            type(username).__name__,
        )

        return super().get_by_natural_key(username)


class ScoutsUser(User):

    objects = ScoutsUserManager()

    #
    # Fields from the groupadmin member record
    #
    group_admin_id: str = models.CharField(max_length=48, db_column="ga_id", blank=True)
    gender: Gender = models.CharField(
        max_length=16, choices=Gender.choices, default=Gender.UNKNOWN
    )
    phone_number: str = models.CharField(max_length=48, blank=True)
    membership_number: str = models.CharField(max_length=48, blank=True)
    customer_number: str = models.CharField(max_length=48, blank=True)
    birth_date: date = models.DateField(blank=True, null=True)

    #
    # Convenience fields to avoid a profile call to groupadmin at every authentication event.
    #
    last_authenticated: datetime = TimezoneAwareDateTimeField(default=datetime.now)
    last_refreshed: datetime = TimezoneAwareDateTimeField(default=datetime.now)
    last_updated: datetime = TimezoneAwareDateTimeField(default=datetime.now)
    last_updated_groups: datetime = TimezoneAwareDateTimeField(default=datetime.now)
    last_updated_funtions: datetime = TimezoneAwareDateTimeField(default=datetime.now)

    #
    # Fields inherited from scouts_auth.auth.models.User that may need to be updated after a call to groupadmin
    #
    # first_name = models.CharField(max_length=124, blank=True)
    # last_name = models.CharField(max_length=124, blank=True)
    # email = models.EmailField(blank=True)

    # Persisted fields
    persisted_scouts_groups: List[ScoutsGroup] = models.ManyToManyField(
        ScoutsGroup, related_name="user"
    )
    persisted_scouts_functions: List[ScoutsFunction] = models.ManyToManyField(
        ScoutsFunction, related_name="user"
    )

    #
    # Locally cached, non-persisted fields
    #
    scouts_groups: List[AbstractScoutsGroup] = []
    addresses: List[AbstractScoutsAddress] = []
    functions: List[AbstractScoutsFunction] = []
    group_specific_fields: List[AbstractScoutsGroupSpecificField] = []
    links: List[AbstractScoutsLink] = []

    #
    # The active access token, provided by group admin oidc
    #
    access_token: str = ""

    #
    # Some shortcut fields
    #
    is_administrator = False
    is_district_commissioner = False

    @property
    def fully_loaded(self) -> bool:
        return self.is_fully_loaded

    @fully_loaded.setter
    def fully_loaded(self, is_fully_loaded: bool):
        self.is_fully_loaded = is_fully_loaded

    def get_function_codes(self) -> List[str]:
        return [function.code for function in self.functions]

    def get_group_functions(self) -> List[Tuple]:
        return [
            (function.group.group_admin_id, function.code)
            for function in self.functions
        ]

    def get_group_names(self) -> List[str]:
        return [group.group_admin_id for group in self.scouts_groups]

    def has_role_section_leader(self, group: AbstractScoutsGroup) -> bool:
        """
        Determines if the user is a section leader based on a function in the specified group
        """
        for function in self.functions:
            if function.is_section_leader(group):
                return True
        return False

    def get_section_leader_groups(self) -> List[AbstractScoutsGroup]:
        return [
            group for group in self.scouts_groups if self.has_role_section_leader(group)
        ]

    def has_role_group_leader(self, group: AbstractScoutsGroup) -> bool:
        """
        Determines if the user is a group leader based on a function in the specified group
        """
        for function in self.functions:
            if function.is_group_leader(group):
                return True

        return False

    def get_group_leader_groups(self) -> List[AbstractScoutsGroup]:
        return [
            group for group in self.scouts_groups if self.has_role_group_leader(group)
        ]

    def has_role_district_commissioner(self) -> bool:
        """
        Determines if the user is a district commissioner based on a function code
        """
        for function in self.functions:
            if function.is_district_commissioner():
                return True
        return False

    def has_role_administrator(self) -> bool:
        """
        Determines if the user is an administrative worker based on membership of an administrative group
        """
        if any(
            name in self.get_group_names()
            for name in GroupadminSettings.get_administrator_groups()
        ):
            self.is_administrator = True
        return self.is_administrator

    @property
    def permissions(self):
        return self.get_all_permissions()

    def __str__(self):
        return (
            super().__str__()
            + "group_admin_id({}), gender ({}), phone_number({}), membership_number({}), customer_number({}), birth_date({}), scouts_groups({}), addresses({}), functions({}), group_specific_fields({}), links({})"
        ).format(
            self.group_admin_id,
            self.gender,
            self.phone_number,
            self.membership_number,
            self.customer_number,
            self.birth_date,
            ", ".join(group.group_admin_id for group in self.scouts_groups)
            if self.scouts_groups
            else "[]",
            ", ".join(address.to_descriptive_string() for address in self.addresses)
            if self.addresses
            else "[]",
            ", ".join(function.to_descriptive_string() for function in self.functions)
            if self.functions
            else "[]",
            ", ".join(
                str(group_specific_field)
                for group_specific_field in self.group_specific_fields
            )
            if self.group_specific_fields
            else "[]",
            ", ".join(str(link) for link in self.links) if self.links else "[]",
        )

    def to_descriptive_string(self):
        return (
            "{}\n"
            "{:<24}: {}\n"  # username
            "{:<24}: {}\n"  # first_name
            "{:<24}: {}\n"  # last_name
            "{:<24}: {}\n"  # gender
            "{:<24}: {}\n"  # birth_date
            "{:<24}: {}\n"  # phone_number
            "{:<24}: {}\n"  # email
            "{:<24}: {}\n"  # group_admin_id
            "{:<24}: {}\n"  # membership_number
            "{:<24}: {}\n"  # customer_number
            "{:<24}: {}\n"  # addresses
            "{:<24}: {}\n"  # functions
            "{:<24}: {}\n"  # permissions
            "{:<24}: {}\n"  # auth groups
            "{:<24}: {}\n"  # scouts groups
            "{:<24}: {}\n"  # administrator ?
            "{:<24}: {}\n"  # district commissioner ?
            "{:<24}: {}\n"  # group leader
            "{:<24}: {}\n"  # section leader
            "{:<24}: {}\n"  # last authenticated
            "{:<24}: {}\n"  # last refreshed
            "{:<24}: {}\n"  # last updated
            "{:<24}: {}\n"  # last updated groups
            "{:<24}: {}\n"  # last updated functions
        ).format(
            "USER INFO",
            "username",
            self.username,
            "first_name",
            self.first_name,
            "last_name",
            self.last_name,
            "gender",
            self.gender,
            "birth_date",
            self.birth_date,
            "phone_number",
            self.phone_number,
            "email",
            self.email,
            "group_admin_id",
            self.group_admin_id,
            "membership_number",
            self.membership_number,
            "customer_number",
            self.customer_number,
            "addresses",
            " || ".join(address.to_descriptive_string() for address in self.addresses),
            "functions",
            # " || ".join(
            #     function.to_descriptive_string() for function in self.functions
            # ),
            len(self.functions),
            "PERMISSIONS",
            ", ".join(permission for permission in self.get_all_permissions()),
            "AUTH GROUPS",
            ", ".join(group.name for group in self.groups.all()),
            "SCOUTS GROUPS",
            ", ".join(
                (group.name + "(" + group.group_admin_id + ")")
                for group in self.scouts_groups
            ),
            "ADMINISTRATOR ?",
            self.has_role_administrator(),
            "DISTRICT COMMISSIONER ?",
            self.has_role_district_commissioner(),
            "GROUP LEADER",
            ", ".join(group.group_admin_id for group in self.get_group_leader_groups()),
            "SECTION LEADER",
            ", ".join(
                group.group_admin_id for group in self.get_section_leader_groups()
            ),
            "last authenticated",
            self.last_authenticated,
            "last refreshed",
            self.last_refreshed,
            "last updated",
            self.last_updated,
            "last updated groups",
            self.last_updated_groups,
            "last updated functions",
            self.last_updated_functions,
        )
