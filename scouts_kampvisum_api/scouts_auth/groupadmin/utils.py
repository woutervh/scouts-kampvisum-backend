import logging
import datetime
from typing import List

from django.conf import settings
from django.utils import timezone


logger = logging.getLogger(__name__)


class SettingsHelper:
    """Convenience class with static methods to easily distinguish what settings are required for dependent packages."""

    @staticmethod
    def is_debug() -> List[str]:
        return getattr(settings, "DEBUG", False)

    @staticmethod
    def get_group_admin_base_url(default_value=None):
        return getattr(settings, "GROUP_ADMIN_BASE_URL", default_value)

    @staticmethod
    def get_group_admin_allowed_calls_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_ALLOWED_CALLS_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_profile_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_PROFILE_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_search_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_MEMBER_SEARCH_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_detail_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_MEMBER_DETAIL_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_group_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_GROUP_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_functions_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_FUNCTIONS_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_list_endpoint(default_value=None):
        attr = getattr(settings, "GROUP_ADMIN_MEMBER_LIST_ENDPOINT", default_value)
        logger.debug("ENDPOINT: %s", attr)
        return attr

    @staticmethod
    def get_activity_epoch(default_value=None):
        # The "activity epoch" after which a member is deemed a past active member
        return getattr(settings, "ACTIVITY_EPOCH", 3)

    @staticmethod
    def get_camp_registration_epoch(default_value=None):
        # The date after which a new camp registration is considered to be in the next camp year
        value = getattr(settings, "CAMP_REGISTRATION_EPOCH")
        month, day = value.split("-")

        return (int(month), int(day))

    @staticmethod
    def get_camp_registration_epoch_date(default_value=None):
        month, day = SettingsHelper.get_camp_registration_epoch(default_value)

        return datetime.datetime(timezone.now().date().year, month, day).date()

    @staticmethod
    def get_responsibility_epoch(default_value=None):
        # A setting that determines when the camp responsibles have to take extra action if a responsible person changes.
        value = getattr(settings, "RESPONSIBILITY_EPOCH")
        month, day = value.split("-")

        return (int(month), int(day))

    @staticmethod
    def get_responsibility_epoch_date(default_value=None):
        month, day = SettingsHelper.get_responsibility_epoch(default_value)

        return datetime.datetime(timezone.now().date().year, month, day).date()

    @staticmethod
    def get_administrator_groups() -> List[str]:
        return settings.KNOWN_ADMIN_GROUPS

    @staticmethod
    def get_test_groups() -> List[str]:
        return settings.KNOWN_TEST_GROUPS

    @staticmethod
    def get_roles() -> List[str]:
        return settings.KNOWN_ROLES

    @staticmethod
    def get_section_leader_identifier() -> str:
        return settings.SECTION_LEADER_IDENTIFIER
