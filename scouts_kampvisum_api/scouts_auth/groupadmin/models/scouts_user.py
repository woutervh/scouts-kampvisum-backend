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

    _scouts_functions: List[ScoutsFunction] = []
    _scouts_function_names: List[str] = None
    _scouts_function_descriptions: List[str] = None

    _scouts_groups: List[ScoutsGroup] = []
    _scouts_group_names: List[str] = None
    _scouts_groups_with_underlying_groups: List[ScoutsGroup] = []
    _scouts_leader_groups: List[ScoutsGroup] = []
    _scouts_leader_group_names: List[str] = None
    _scouts_section_leader_groups: List[ScoutsGroup] = None
    _scouts_section_leader_group_names: List[str] = None
    _scouts_group_leader_groups: List[ScoutsGroup] = None
    _scouts_group_leader_group_names: List[str] = None
    _scouts_district_commissioner_groups: List[ScoutsGroup] = None
    _scouts_district_commissioner_group_names: List[str] = None
    _scouts_shire_president_groups: List[ScoutsGroup] = None
    _scouts_shire_president_group_names: List[str] = None

    #
    # The active access token, provided by group admin oidc
    #
    access_token: str = ""

    def clear_scouts_functions(self):
        self._scouts_functions = []
        self._scouts_function_names = None
        self._scouts_function_descriptions = None

    def clear_scouts_groups(self):
        self._scouts_groups = []
        self._scouts_group_names = None
        self._scouts_groups_with_underlying_groups = []
        self._scouts_leader_groups = []
        self._scouts_leader_group_names = None
        self._scouts_section_leader_groups = None
        self._scouts_section_leader_group_names = None
        self._scouts_group_leader_groups = None
        self._scouts_group_leader_group_names = None
        self._scouts_district_commissioner_groups = None
        self._scouts_district_commissioner_group_names = None
        self._scouts_shire_president_groups = None
        self._scouts_shire_president_group_names = None

    def has_scouts_function(self, scouts_function: ScoutsFunction):
        for existing_function in self._scouts_functions:
            if (
                existing_function.group_admin_id == scouts_function.group_admin_id
                and existing_function.scouts_group.group_admin_id == scouts_function.scouts_group.group_admin_id
            ):
                return True
        return False

    def add_scouts_function(self, scouts_function: ScoutsFunction):
        if not self.has_scouts_function(scouts_function=scouts_function):
            self._scouts_functions.append(scouts_function)
            self._scouts_functions.sort(
                key=lambda x: x.scouts_group.group_admin_id)

    def get_scouts_functions(self) -> List[ScoutsFunction]:
        return self._scouts_functions

    def get_scouts_function_names(self) -> List[str]:
        if not self._scouts_function_names:
            self._scouts_function_names = [
                scouts_function.group_admin_id for scouts_function in self._scouts_functions]
        return self._scouts_function_names

    def get_scouts_function_descriptions(self) -> List[str]:
        if not self._scouts_function_descriptions:
            self._scouts_function_descriptions = [
                scouts_function.description for scouts_function in self._scouts_functions]
        return self._scouts_function_descriptions

    def add_scouts_group(self, scouts_group: ScoutsGroup):
        if scouts_group.group_admin_id not in self.get_scouts_group_names():
            self._scouts_groups.append(scouts_group)
            self._scouts_groups.sort(key=lambda x: x.group_admin_id)

    def get_scouts_group(self, group_admin_id: str, raise_exception: bool = False) -> ScoutsGroup:
        for scouts_group in self._scouts_groups:
            if scouts_group.group_admin_id == group_admin_id:
                return scouts_group

        if raise_exception:
            raise InvalidArgumentException(
                f"[{self.username}] This user doesn't have access to group {group_admin_id}")

        return None

    def get_scouts_groups(self, include_underlying_groups=False) -> List[ScoutsGroup]:
        if not include_underlying_groups:
            return self._scouts_groups
        return self.get_scouts_groups_with_underlying_groups()

    def get_scouts_groups_with_underlying_groups(self) -> List[ScoutsGroup]:
        if not self._scouts_groups_with_underlying_groups:
            combined_groups: List[ScoutsGroup] = list()
            for scouts_group in self._scouts_groups:
                if scouts_group.group_admin_id not in combined_groups:
                    combined_groups.append(scouts_group)

                    if scouts_group.has_child_groups():
                        child_groups = scouts_group.get_child_groups()
                        for child_group in child_groups:
                            child_scouts_group = self.get_scouts_group(
                                group_admin_id=child_group, raise_exception=True)

                            if child_scouts_group and child_scouts_group not in combined_groups:
                                combined_groups.append(child_scouts_group)
            combined_groups = list(set(combined_groups))
            combined_groups.sort(key=lambda x: x.group_admin_id)
            self._scouts_groups_with_underlying_groups = combined_groups
        return self._scouts_groups_with_underlying_groups

    def get_scouts_group_names(self) -> List[str]:
        if not self._scouts_group_names:
            self._scouts_group_names = [
                group.group_admin_id for group in self._scouts_groups]
        return self._scouts_group_names

    def get_roles_for_group(self, scouts_group: ScoutsGroup = None, group_admin_id: str = None) -> List[str]:
        if not scouts_group and not group_admin_id:
            raise InvalidArgumentException(
                "Can't determine roles for group without a scouts group or group admin id")

        if not scouts_group:
            scouts_group = self.get_scouts_group(
                group_admin_id=group_admin_id, raise_exception=True)

        if not scouts_group:
            return []

        roles: List[str] = []
        for scouts_function in self._scouts_functions:
            if (
                # Role in the specified group
                scouts_function.scouts_group == scouts_group
                # Role as an underlying group, e.g. DC defined on X9000D -> DC for X9002G
                or (
                    (
                        scouts_function.is_district_commissioner_function()
                        or scouts_function.is_shire_president_function()
                    )
                    and scouts_group.group_admin_id in scouts_function.scouts_group.get_child_groups()
                )
            ):
                role = scouts_function.get_role_name()
                if role not in roles:
                    roles.append(scouts_function.get_role_name())

        return roles

    def has_role_leader(self, scouts_group: ScoutsGroup = None, group_admin_id: str = None, include_inactive: bool = False) -> bool:
        """
        Determines if the user is has a leader function in the specified group
        """
        return self._has_role(
            scouts_group=scouts_group,
            group_admin_id=group_admin_id,
            role="leader",
            scouts_function_name="is_leader_function",
            include_inactive=include_inactive,)

    def get_scouts_leader_groups(self) -> List[ScoutsGroup]:
        if not self._scouts_leader_groups:
            self._scouts_leader_groups = [
                scouts_group
                for scouts_group in self._scouts_groups
                if self.has_role_leader(scouts_group=scouts_group)
            ]
        return self._scouts_leader_groups

    def get_scouts_leader_group_names(self) -> List[str]:
        if not self._scouts_leader_group_names:
            self._scouts_leader_group_names = [
                scouts_group.group_admin_id for scouts_group in self.get_scouts_leader_groups()]
        return self._scouts_leader_group_names

    def has_role_section_leader(self, scouts_group: ScoutsGroup = None, group_admin_id: str = None, include_inactive: bool = False) -> bool:
        """
        Determines if the user is a section leader based on a function in the specified group
        """
        return self._has_role(
            scouts_group=scouts_group,
            group_admin_id=group_admin_id,
            role="section leader",
            scouts_function_name="is_section_leader_function",
            include_inactive=include_inactive,)

    def get_scouts_section_leader_groups(self) -> List[ScoutsGroup]:
        if not self._scouts_section_leader_groups:
            self._scouts_section_leader_groups = [
                scouts_group
                for scouts_group in self._scouts_groups
                if self.has_role_section_leader(scouts_group=scouts_group)
            ]
        return self._scouts_section_leader_groups

    def get_scouts_section_leader_group_names(self) -> List[str]:
        if not self._scouts_section_leader_group_names:
            self._scouts_section_leader_group_names = [
                scouts_group.group_admin_id for scouts_group in self.get_scouts_section_leader_groups()]
        return self._scouts_section_leader_group_names

    def has_role_group_leader(self, scouts_group: ScoutsGroup = None, group_admin_id: str = None, include_inactive: bool = False) -> bool:
        """
        Determines if the user is a group leader based on a function in the specified group
        """
        return self._has_role(
            scouts_group=scouts_group,
            group_admin_id=group_admin_id,
            role="group leader",
            scouts_function_name="is_group_leader_function",
            include_inactive=include_inactive,)

    def get_scouts_group_leader_groups(self) -> List[ScoutsGroup]:
        if not self._scouts_group_leader_groups:
            self._scouts_group_leader_groups = [
                scouts_group
                for scouts_group in self._scouts_groups
                if self.has_role_group_leader(scouts_group=scouts_group)
            ]
        return self._scouts_group_leader_groups

    def get_scouts_group_leader_group_names(self) -> List[str]:
        if not self._scouts_group_leader_group_names:
            self._scouts_group_leader_group_names = [
                scouts_group.group_admin_id for scouts_group in self.get_scouts_group_leader_groups()]
        return self._scouts_group_leader_group_names

    def has_role_district_commissioner(self, scouts_group: ScoutsGroup = None, group_admin_id: str = None, include_inactive: bool = False) -> bool:
        """
        Determines if the user is a district commissioner based on a function code
        """
        return self._has_role(
            scouts_group=scouts_group,
            group_admin_id=group_admin_id,
            role="district commissioner",
            scouts_function_name="is_district_commissioner_function",
            include_inactive=include_inactive,
            for_underlying_scouts_groups=True,)

    def get_scouts_district_commissioner_groups(self) -> List[ScoutsGroup]:
        if not self._scouts_district_commissioner_groups:
            self._scouts_district_commissioner_groups = [
                scouts_group
                for scouts_group in self._scouts_groups
                if self.has_role_district_commissioner(scouts_group=scouts_group)
            ]
        return self._scouts_district_commissioner_groups

    def get_scouts_district_commissioner_group_names(self) -> List[str]:
        if not self._scouts_district_commissioner_group_names:
            self._scouts_district_commissioner_group_names = [
                scouts_group.group_admin_id for scouts_group in self.get_scouts_district_commissioner_groups()]
        return self._scouts_district_commissioner_group_names

    def has_role_shire_president(self, scouts_group: ScoutsGroup = None, group_admin_id: str = None, include_inactive: bool = False) -> bool:
        """
        Determines if the user is a shire president (gouwvoorzitter) based on a function code
        """
        return self._has_role(
            scouts_group=scouts_group,
            group_admin_id=group_admin_id,
            role="shire president",
            scouts_function_name="is_shire_president_function",
            include_inactive=include_inactive,
            for_underlying_scouts_groups=True,)

    def get_scouts_shire_president_groups(self) -> List[ScoutsGroup]:
        if not self._scouts_shire_president_groups:
            self._scouts_shire_president_groups = [
                scouts_group
                for scouts_group in self._scouts_groups
                if self.has_role_shire_president(scouts_group=scouts_group)
            ]
        return self._scouts_shire_president_groups

    def get_scouts_shire_president_group_names(self) -> List[str]:
        if not self._scouts_shire_president_group_names:
            self._scouts_shire_president_group_names = [
                scouts_group.group_admin_id for scouts_group in self.get_scouts_shire_president_groups()]
        return self._scouts_shire_president_group_names

    def has_role_administrator(self) -> bool:
        """
        Determines if the user is an administrative worker based on membership of an administrative group
        """
        if any(
            name in self.get_scouts_group_names()
            for name in GroupAdminSettings.get_administrator_groups()
        ):
            return True
        return False

    def _has_role(
            self,
            role: str,
            scouts_function_name: str,
            scouts_group: ScoutsGroup = None,
            group_admin_id: str = None,
            ignore_group: bool = False,
            for_underlying_scouts_groups=False,
            include_inactive: bool = False) -> bool:
        """
        Determines if the user is has the specified function in the specified group
        """

        # logger.debug(f"Determining if user has role {role}", user=self)

        if not scouts_group and not group_admin_id and not ignore_group:
            raise InvalidArgumentException(
                f"Can't determine {role} role without a group or group admin id")

        if not scouts_group:
            scouts_group = self.get_scouts_group(
                group_admin_id=group_admin_id, raise_exception=True)

        if not scouts_group:
            return False

        for scouts_function in self._scouts_functions:
            if not include_inactive and not scouts_function.is_active_function():
                return False

            if getattr(scouts_function, scouts_function_name)():
                if not for_underlying_scouts_groups:
                    if scouts_function.scouts_group.group_admin_id == scouts_group.group_admin_id:
                        return True
                else:
                    if scouts_function.scouts_group.has_child_groups():
                        if scouts_group.group_admin_id in scouts_function.scouts_group.get_child_groups():
                            return True

        return False

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
        shire_president_groups: List[ScoutsGroup] = self.get_scouts_shire_president_groups(
        )
        district_commissioner_groups: List[ScoutsGroup] = self.get_scouts_district_commissioner_groups(
        )
        group_leader_groups: List[ScoutsGroup] = self.get_scouts_group_leader_groups(
        )
        section_leader_groups: List[ScoutsGroup] = self.get_scouts_section_leader_groups(
        )

        scouts_group_names: List[str] = [
            scouts_group.group_admin_id for scouts_group in self.get_scouts_groups_with_underlying_groups()]
        scouts_leader_group_names: List[str] = self.get_scouts_leader_group_names(
        )

        descriptive_scouts_functions: List[List[str]] = [
            scouts_function.code + "(" + scouts_function.scouts_group.group_admin_id + (": LEIDING" if scouts_function.is_leader_function() else "") + ")" for scouts_function in sorted(self._scouts_functions, key=lambda x: x.scouts_group.group_admin_id)]

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
            "{:<24}: {}\n"  # is_active
            "{:<24}: {}\n"  # is_authenticated
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
            "username", self.username,
            "first_name", self.first_name,
            "last_name", self.last_name,
            "gender", self.gender,
            "birth_date", self.birth_date,
            "phone_number", self.phone_number,
            "email", self.email,
            "group_admin_id", self.group_admin_id,
            "membership_number", self.membership_number,
            "customer_number", self.customer_number,
            "IS_ACTIVE", self.is_active,
            "IS_AUTHENTICATED", self.is_authenticated,
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
            "KNOWN_ADMIN_GROUPS", SettingsHelper.get_list(
                "KNOWN_ADMIN_GROUPS"),
            "Administrator groups", GroupAdminSettings.get_administrator_groups(),
            "KNOWN_TEST_GROUPS", SettingsHelper.get_list("KNOWN_TEST_GROUPS"),
            "Test groups", GroupAdminSettings.get_test_groups(),
            "DEBUG", SettingsHelper.get_bool("DEBUG"),
            "IS_ACCEPTANCE", SettingsHelper.get_bool("IS_ACCEPTANCE"),
            "Is debug ?", GroupAdminSettings.is_debug(),
            "Is acceptance ?", GroupAdminSettings.is_acceptance(),
            "Is test ?", GroupAdminSettings.is_test(),
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
