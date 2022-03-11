import datetime
from typing import List

from django.conf import settings
from django.utils import timezone

from scouts_auth.inuits.utils import SettingsHelper

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GroupadminSettings(SettingsHelper):
    """Convenience class with static methods to easily distinguish what settings are required for dependent packages."""

    @staticmethod
    def is_debug() -> List[str]:
        return GroupadminSettings.get_bool("DEBUG", False)

    @staticmethod
    def get_group_admin_base_url(default_value=None):
        return GroupadminSettings.get("GROUP_ADMIN_BASE_URL", default_value)

    @staticmethod
    def get_group_admin_allowed_calls_endpoint(default_value=None):
        return GroupadminSettings.get(
            "GROUP_ADMIN_ALLOWED_CALLS_ENDPOINT", default_value
        )

    @staticmethod
    def get_group_admin_profile_endpoint(default_value=None):
        return GroupadminSettings.get("GROUP_ADMIN_PROFILE_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_search_endpoint(default_value=None):
        return GroupadminSettings.get(
            "GROUP_ADMIN_MEMBER_SEARCH_ENDPOINT", default_value
        )

    @staticmethod
    def get_group_admin_member_detail_endpoint(default_value=None):
        return GroupadminSettings.get(
            "GROUP_ADMIN_MEMBER_DETAIL_ENDPOINT", default_value
        )

    @staticmethod
    def get_group_admin_group_endpoint(default_value=None):
        return GroupadminSettings.get("GROUP_ADMIN_GROUP_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_functions_endpoint(default_value=None):
        return GroupadminSettings.get("GROUP_ADMIN_FUNCTIONS_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_list_endpoint(default_value=None):
        return GroupadminSettings.get("GROUP_ADMIN_MEMBER_LIST_ENDPOINT", default_value)

    @staticmethod
    def include_inactive_members_in_search(default_value=False):
        return GroupadminSettings.get_bool(
            "INCLUDE_INACTIVE_MEMBERS_IN_SEARCH", default_value
        )

    @staticmethod
    def get_activity_epoch(default_value=None):
        # The "activity epoch" after which a member is deemed a past active member
        return GroupadminSettings.get_int("ACTIVITY_EPOCH", 3)

    @staticmethod
    def get_camp_registration_epoch(default_value=None):
        # The date after which a new camp registration is considered to be in the next camp year
        value = GroupadminSettings.get("CAMP_REGISTRATION_EPOCH", default_value)
        month, day = value.split("-")

        return (int(month), int(day))

    @staticmethod
    def get_camp_registration_epoch_date(default_value=None):
        month, day = GroupadminSettings.get_camp_registration_epoch(default_value)

        return datetime.datetime(timezone.now().date().year, month, day).date()

    @staticmethod
    def get_responsibility_epoch(default_value=None):
        # A setting that determines when the camp responsibles have to take extra action if a responsible person changes.
        value = GroupadminSettings.get("RESPONSIBILITY_EPOCH", default_value)
        month, day = value.split("-")

        return (int(month), int(day))

    @staticmethod
    def get_responsibility_epoch_date(default_value=None):
        month, day = GroupadminSettings.get_responsibility_epoch(default_value)

        return datetime.datetime(timezone.now().date().year, month, day).date()

    @staticmethod
    def get_administrator_groups() -> List[str]:
        return SettingsHelper.get("KNOWN_ADMIN_GROUPS")

    @staticmethod
    def get_test_groups() -> List[str]:
        return SettingsHelper.get("KNOWN_TEST_GROUPS")

    @staticmethod
    def get_roles() -> List[str]:
        return SettingsHelper.get("KNOWN_ROLES")

    @staticmethod
    def get_section_leader_identifier() -> str:
        return SettingsHelper.get("SECTION_LEADER_IDENTIFIER")

    @staticmethod
    def get_group_gender_identifier_male() -> str:
        return SettingsHelper.get("GROUP_GENDER_IDENTIFIER_MALE")

    @staticmethod
    def get_group_gender_identifier_female() -> str:
        return SettingsHelper.get("GROUP_GENDER_IDENTIFIER_FEMALE")
