from typing import List, Tuple
from datetime import date, datetime

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import UserManager

from scouts_auth.auth.exceptions import InvalidArgumentException
from scouts_auth.auth.models import User

from scouts_auth.groupadmin.models import (
    AbstractScoutsMember,
    AbstractScoutsAddress,
    AbstractScoutsFunctionDescription,
    AbstractScoutsFunction,
    AbstractScoutsGroupSpecificField,
    AbstractScoutsLink,
    AbstractScoutsGroup,
    ScoutsGroup,
    ScoutsFunction,
)
from scouts_auth.groupadmin.models.fields import GroupAdminIdField
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.inuits.models import Gender
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    RequiredCharField,
    DefaultCharField,
    TimezoneAwareDateTimeField,
)

from scouts_auth.inuits.utils import SettingsHelper


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
            except Exception:
                pass

        if username:
            try:
                return self.get_by_natural_key(username)
            except Exception:
                pass

        if group_admin_id:
            try:
                return self.get_queryset().get(group_admin_id=group_admin_id)
            except Exception:
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

    group_admin_id: str = GroupAdminIdField()
    gender: Gender = DefaultCharField(
        max_length=16, choices=Gender.choices, default=Gender.UNKNOWN
    )
    phone_number: str = OptionalCharField(max_length=48)
    membership_number: str = OptionalCharField(max_length=48)
    customer_number: str = OptionalCharField(max_length=48)
    birth_date: date = models.DateField(blank=True, null=True)

    scouts_groups: List[ScoutsGroup] = []
    scouts_leader_groups: List[ScoutsGroup] = []
    scouts_functions: List[ScoutsFunction] = []

    #
    # The active access token, provided by group admin oidc
    #
    access_token: str = ""

    def add_scouts_function(self, scouts_function: ScoutsFunction):
        if scouts_function.group_admin_id not in self.get_scouts_function_names():
            logger.debug(
                f"Adding function {scouts_function.code} ({scouts_function.__class__.__name__} - {len(self.scouts_functions)})")
            self.scouts_functions.append(scouts_function)
            self.scouts_functions.sort(key=lambda x: x.group_admin_id)

    def get_scouts_function_names(self) -> List[str]:
        return [scouts_function.group_admin_id for scouts_function in self.scouts_functions]

    def get_scouts_function_descriptions(self) -> List[str]:
        return [scouts_function.description for scouts_function in self.scouts_functions]

    def add_scouts_group(self, scouts_group: ScoutsGroup):
        if scouts_group.group_admin_id not in self.get_scouts_group_names():
            logger.debug(
                f"Adding scouts group {scouts_group.group_admin_id} ({scouts_group.__class__.__name__} - {len(self.scouts_groups)})")
            self.scouts_groups.append(scouts_group)
            self.scouts_groups.sort(key=lambda x: x.group_admin_id)

    def get_scouts_group(self, group_admin_id: str, raise_exception: bool = False) -> ScoutsGroup:
        for scouts_group in self.scouts_groups:
            if scouts_group.group_admin_id == group_admin_id:
                return scouts_group

        if raise_exception:
            raise InvalidArgumentException(
                "This user doesn't have access to group {group_admin_id}", user=self)

        return None

    def get_scouts_group_names(self) -> List[str]:
        return [group.group_admin_id for group in self.scouts_groups]

    def get_function_codes(self) -> List[str]:
        return [function.code for function in self.functions]

    def get_group_functions(self) -> List[Tuple]:
        return []

    def get_group_names(self) -> List[str]:
        return [group.group_admin_id for group in self.scouts_groups]

    def has_role_leader(self, scouts_group: ScoutsGroup = None, group_admin_id: str = None) -> bool:
        """
        Determines if the user is has a leader function in the specified group
        """

        if not scouts_group and not group_admin_id:
            raise InvalidArgumentException(
                "Can't determine leader role without a group or group admin id")

        if not scouts_group:
            scouts_group = self.get_scouts_group(
                group_admin_id=group_admin_id, raise_exception=True)

        for scouts_function in self.scouts_functions:
            if (
                scouts_function.scouts_group.group_admin_id == scouts_group.group_admin_id
                and scouts_function.is_section_leader_function()
            ):
                return True

        return False

    def get_scouts_leader_groups(self) -> List[ScoutsGroup]:
        return [
            scouts_group
            for scouts_group in self.scouts_groups
            if self.has_role_leader(scouts_group=scouts_group)
        ]

    def get_scouts_leader_group_names(self) -> List[str]:
        return [scouts_group.group_admin_id for scouts_group in self.get_scouts_leader_groups()]

    def has_role_section_leader(self, scouts_group: ScoutsGroup = None, group_admin_id: str = None) -> bool:
        """
        Determines if the user is a section leader based on a function in the specified group
        """

        if not scouts_group and not group_admin_id:
            raise InvalidArgumentException(
                "Can't determine section leader role without a group or group admin id")

        if not scouts_group:
            scouts_group = self.get_scouts_group(
                group_admin_id=group_admin_id, raise_exception=True)

        for scouts_function in self.scouts_functions:
            if (
                scouts_function.scouts_group.group_admin_id == scouts_group.group_admin_id
                and scouts_function.is_section_leader_function()
            ):
                return True

        return False

    def get_section_leader_groups(self) -> List[ScoutsGroup]:
        return [
            scouts_group
            for scouts_group in self.scouts_groups
            if self.has_role_section_leader(scouts_group=scouts_group)
        ]

    def has_role_group_leader(self, scouts_group: ScoutsGroup) -> bool:
        """
        Determines if the user is a group leader based on a function in the specified group
        """

        if not scouts_group and not group_admin_id:
            raise InvalidArgumentException(
                "Can't determine group leader role without a group or group admin id")

        if not scouts_group:
            scouts_group = self.get_scouts_group(
                group_admin_id=group_admin_id, raise_exception=True)

        for scouts_function in self.scouts_functions:
            if (
                scouts_function.scouts_group.group_admin_id == scouts_group.group_admin_id
                and scouts_function.is_group_leader_function()
            ):
                return True

        return False

    def get_group_leader_groups(self) -> List[ScoutsGroup]:
        return [
            scouts_group
            for scouts_group in self.scouts_groups
            if self.has_role_group_leader(scouts_group=scouts_group)
        ]

    def has_role_district_commissioner(self, scouts_group: ScoutsGroup = None) -> bool:
        """
        Determines if the user is a district commissioner based on a function code
        """

        if not scouts_group and not group_admin_id:
            raise InvalidArgumentException(
                "Can't determine district commissioner role without a group or group admin id")

        if not scouts_group:
            scouts_group = self.get_scouts_group(
                group_admin_id=group_admin_id, raise_exception=True)

        for scouts_function in self.scouts_functions:
            if (
                scouts_function.scouts_group.group_admin_id == scouts_group.group_admin_id
                and scouts_function.is_district_commissioner_function()
            ):
                return True

        return False

    def get_district_commissioner_groups(self) -> List[ScoutsGroup]:
        return [
            scouts_group
            for scouts_group in self.scouts_groups
            if self.has_role_district_commissioner(scouts_group=scouts_group)
        ]

    def has_role_shire_president(self, scouts_group: ScoutsGroup = None) -> bool:
        """
        Determines if the user is a shire president (gouwvoorzitter) baed on a function code
        """

        if not scouts_group and not group_admin_id:
            raise InvalidArgumentException(
                "Can't determine shire president role without a group or group admin id")

        if not scouts_group:
            scouts_group = self.get_scouts_group(
                group_admin_id=group_admin_id, raise_exception=True)

        for scouts_function in self.scouts_functions:
            if (
                scouts_function.scouts_group.group_admin_id == scouts_group.group_admin_id
                and scouts_function.is_shire_president_function()
            ):
                return True

        return False

    def get_shire_president_groups(self) -> List[ScoutsGroup]:
        return [
            scouts_group
            for scouts_group in self.scouts_groups
            if self.has_role_shire_president(scouts_group=scouts_group)
        ]

    def has_role_administrator(self) -> bool:
        """
        Determines if the user is an administrative worker based on membership of an administrative group
        """
        if any(
            name in self.get_group_names()
            for name in GroupAdminSettings.get_administrator_groups()
        ):
            return True
        return False

    @property
    def permissions(self):
        return self.get_all_permissions()

    def __str__(self):
        return (
            f"group_admin_id ({self.group_admin_id}), "
            f"gender ({self.gender}), "
            f"phone_number ({self.phone_number}), "
            f"membership_number ({self.membership_number}), "
            f"customer_number ({self.customer_number}), "
            f"birth_date ({self.birth_date}), "
            f"scouts_groups ({', '.join(self.get_group_names() if self.scouts_groups else [])}), "
            f"functions ({', '.join(function.to_descriptive_string() for function in self.functions) if self.functions else '[]'})"
        )

    def to_descriptive_string(self):
        groups = self.groups.all()
        shire_president_groups: List[ScoutsGroup] = self.get_shire_president_groups(
        )
        district_commissioner_groups: List[ScoutsGroup] = self.get_district_commissioner_groups(
        )
        group_leader_groups: List[ScoutsGroup] = self.get_group_leader_groups()
        section_leader_groups: List[ScoutsGroup] = self.get_section_leader_groups(
        )

        scouts_group_names: List[str] = self.get_scouts_group_names()
        scouts_leader_group_names: List[str] = self.get_scouts_leader_group_names(
        )

        descriptive_scouts_functions: List[List[str]] = [
            scouts_function.description + "(" + scouts_function.scouts_group.group_admin_id + ")" for scouts_function in self.scouts_functions]

        return (
            "\n------------------------------------------------------------------------------------------------------------------------\n"
            "{}\n"
            "------------------------------------------------------------------------------------------------------------------------\n"
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
            "------------------------------------------------------------------------------------------------------------------------\n"
            "{:<24}: {}\n"  # permissions
            "{:<24}: {}\n"  # auth groups
            "{:<24}: {}\n"  # functions
            "{:<24}: {}\n"  # scouts groups
            "{:<24}: {}\n"  # scouts leader groups
            "{:<24}: {}\n"  # administrator ?
            "{:<24}: {}\n"  # shire president ?
            "{:<24}: {}\n"  # district commissioner ?
            "{:<24}: {}\n"  # group leader
            "{:<24}: {}\n"  # section leader
            "------------------------------------------------------------------------------------------------------------------------\n"
            "{:<24}: {}\n"  # KNOWN_ADMIN_GROUPS
            "{:<24}: {}\n"  # Administrator groups
            "{:<24}: {}\n"  # KNOWN_TEST_GROUPS
            "{:<24}: {}\n"  # Test groups
            "{:<24}: {}\n"  # DEBUG
            "{:<24}: {}\n"  # IS_ACCEPTANCE
            "{:<24}: {}\n"  # Is debug ?
            "{:<24}: {}\n"  # Is acceptance ?
            "{:<24}: {}\n"  # Is test ?
            "------------------------------------------------------------------------------------------------------------------------\n"
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

            "PERMISSIONS",
            ", ".join(permission for permission in self.get_all_permissions())
            if len(self.get_all_permissions()) > 0
            else "None",
            "AUTH GROUPS",
            ", ".join(group.name for group in groups) if len(
                groups) > 0 else "None",
            "SCOUTS FUNCTIONS",
            ", ".join(descriptive_scouts_functions) if len(
                descriptive_scouts_functions) > 0 else "None",
            "SCOUTS GROUPS",
            ", ".join(
                scouts_group_names) if len(scouts_group_names) > 0 else "None",
            "SCOUTS LEADER GROUPS",
            ", ".join(
                scouts_leader_group_names) if len(
                    scouts_leader_group_names) > 0 else "None",
            "ADMINISTRATOR ?",
            self.has_role_administrator(),
            "SHIRE PRESIDENT",
            ", ".join(
                group.group_admin_id for group in shire_president_groups)
            if len(shire_president_groups) > 0
            else "None",
            "DISTRICT COMMISSIONER",
            ", ".join(
                group.group_admin_id for group in district_commissioner_groups)
            if len(district_commissioner_groups) > 0
            else "None",
            "GROUP LEADER",
            ", ".join(group.group_admin_id for group in group_leader_groups)
            if len(group_leader_groups) > 0
            else "None",
            "SECTION LEADER",
            ", ".join(group.group_admin_id for group in section_leader_groups)
            if len(section_leader_groups) > 0
            else "None",
            "KNOWN_ADMIN_GROUPS",
            SettingsHelper.get_list("KNOWN_ADMIN_GROUPS"),
            "Administrator groups",
            GroupAdminSettings.get_administrator_groups(),
            "KNOWN_TEST_GROUPS",
            SettingsHelper.get_list("KNOWN_TEST_GROUPS"),
            "Test groups",
            GroupAdminSettings.get_test_groups(),
            "DEBUG",
            SettingsHelper.get_bool("DEBUG"),
            "IS_ACCEPTANCE",
            SettingsHelper.get_bool("IS_ACCEPTANCE"),
            "Is debug ?",
            GroupAdminSettings.is_debug(),
            "Is acceptance ?",
            GroupAdminSettings.is_acceptance(),
            "Is test ?",
            GroupAdminSettings.is_test(),
        )

    @ staticmethod
    def from_abstract_member(
        user=None,
        abstract_member: AbstractScoutsMember = None
    ):
        if not abstract_member:
            raise ValidationError(
                "Can't construct a ScoutsUser without an AbstractScoutsMember")

        user = user if user else ScoutsUser()

        user.id = abstract_member.group_admin_id
        user.group_admin_id = abstract_member.group_admin_id
        user.gender = (
            abstract_member.gender if abstract_member.gender else Gender.UNKNOWN
        )
        user.phone_number = (
            abstract_member.phone_number if abstract_member.phone_number else ""
        )
        user.membership_number = (
            abstract_member.membership_number
            if abstract_member.membership_number
            else ""
        )
        user.customer_number = (
            abstract_member.customer_number if abstract_member.customer_number else ""
        )
        user.birth_date = (
            abstract_member.birth_date if abstract_member.birth_date else None
        )
        user.first_name = (
            abstract_member.first_name if abstract_member.first_name else ""
        )
        user.last_name = abstract_member.last_name if abstract_member.last_name else ""
        user.email = abstract_member.email

        return user
