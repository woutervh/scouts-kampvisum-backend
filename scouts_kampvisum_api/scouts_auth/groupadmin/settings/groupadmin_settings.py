import datetime
from typing import List

from django.conf import settings
from django.utils import timezone

from scouts_auth.inuits.utils import SettingsHelper

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GroupAdminSettings(SettingsHelper):
    """Convenience class with static methods to easily distinguish what settings are required for dependent packages."""

    @staticmethod
    def is_debug() -> List[str]:
        return GroupAdminSettings.get_bool("DEBUG", False)

    @staticmethod
    def get_username_from_access_token() -> bool:
        return GroupAdminSettings.get_bool("USERNAME_FROM_ACCESS_TOKEN", True)

    @staticmethod
    def get_group_admin_base_url(default_value=None):
        return GroupAdminSettings.get("GROUP_ADMIN_BASE_URL", default_value)

    @staticmethod
    def get_group_admin_allowed_calls_endpoint(default_value=None):
        return GroupAdminSettings.get(
            "GROUP_ADMIN_ALLOWED_CALLS_ENDPOINT", default_value
        )

    @staticmethod
    def get_group_admin_profile_endpoint(default_value=None):
        return GroupAdminSettings.get("GROUP_ADMIN_PROFILE_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_search_endpoint(default_value=None):
        return GroupAdminSettings.get(
            "GROUP_ADMIN_MEMBER_SEARCH_ENDPOINT", default_value
        )

    @staticmethod
    def get_group_admin_member_detail_endpoint(default_value=None):
        return GroupAdminSettings.get(
            "GROUP_ADMIN_MEMBER_DETAIL_ENDPOINT", default_value
        )

    @staticmethod
    def get_group_admin_group_endpoint(default_value=None):
        return GroupAdminSettings.get("GROUP_ADMIN_GROUP_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_functions_endpoint(default_value=None):
        return GroupAdminSettings.get("GROUP_ADMIN_FUNCTIONS_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_list_endpoint(default_value=None):
        return GroupAdminSettings.get("GROUP_ADMIN_MEMBER_LIST_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_list_filtered_endpoint(default_value=None):
        return GroupAdminSettings.get("GROUP_ADMIN_MEMBER_LIST_FILTERED_ENDPOINT", default_value)

    @staticmethod
    def include_inactive_functions_in_profile(default_value=False):
        return GroupAdminSettings.get_bool(
            "INCLUDE_INACTIVE_FUNCTIONS_IN_PROFILE", default_value
        )

    @staticmethod
    def include_only_leader_functions_in_profile(default_value=True):
        return GroupAdminSettings.get_bool(
            "INCLUDE_ONLY_LEADER_FUNCTIONS_IN_PROFILE", default_value
        )

    @staticmethod
    def include_inactive_members_in_search(default_value=False):
        return GroupAdminSettings.get_bool(
            "INCLUDE_INACTIVE_MEMBERS_IN_SEARCH", default_value
        )

    @staticmethod
    def get_base_auth_roles(default_value=[]):
        return GroupAdminSettings.get_list("BASE_AUTH_ROLES", default_value)

    @staticmethod
    def get_activity_epoch(default_value=None):
        # The "activity epoch" after which a member is deemed a past active member
        return GroupAdminSettings.get_int("ACTIVITY_EPOCH", 3)

    @staticmethod
    def get_camp_registration_epoch(default_value=None):
        # The date after which a new camp registration is considered to be in the next camp year
        value = GroupAdminSettings.get(
            "CAMP_REGISTRATION_EPOCH", default_value)
        month, day = value.split("-")

        return (int(month), int(day))

    @staticmethod
    def get_camp_registration_epoch_date(default_value=None):
        month, day = GroupAdminSettings.get_camp_registration_epoch(
            default_value)

        return datetime.datetime(timezone.now().date().year, month, day).date()

    @staticmethod
    def get_responsibility_epoch(default_value=None):
        # A setting that determines when the camp responsibles have to take extra action if a responsible person changes.
        value = GroupAdminSettings.get("RESPONSIBILITY_EPOCH", default_value)
        month, day = value.split("-")

        return (int(month), int(day))

    @staticmethod
    def get_responsibility_epoch_date(default_value=None):
        month, day = GroupAdminSettings.get_responsibility_epoch(default_value)

        return datetime.datetime(timezone.now().date().year, month, day).date()

    @staticmethod
    def get_administrator_groups() -> List[str]:
        return SettingsHelper.get_list("KNOWN_ADMIN_GROUPS")

    @staticmethod
    def get_test_groups() -> List[str]:
        return SettingsHelper.get_list("KNOWN_TEST_GROUPS")

    @staticmethod
    def get_roles() -> List[str]:
        return SettingsHelper.get_list("KNOWN_ROLES")

    @staticmethod
    def get_leadership_status_identifier() -> str:
        return SettingsHelper.get("LEADERSHIP_STATUS_IDENTIFIER")

    @staticmethod
    def get_group_gender_identifier_male() -> str:
        return SettingsHelper.get("GROUP_GENDER_IDENTIFIER_MALE")

    @staticmethod
    def get_group_gender_identifier_female() -> str:
        return SettingsHelper.get("GROUP_GENDER_IDENTIFIER_FEMALE")

    @staticmethod
    def get_camp_responsible_min_age() -> int:
        return SettingsHelper.get_int("CAMP_RESPONSIBLE_MIN_AGE")
