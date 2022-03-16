import datetime

from django.conf import settings
from django.utils import timezone

from scouts_auth.auth.settings import OIDCSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class OIDCUserHelper:
    @staticmethod
    def _requires_loading(last_updated: datetime, minutes_before_refresh: int):
        now: timezone.datetime = timezone.now()

        delta_seconds = int(now.timestamp()) - int(last_updated.timestamp())

        return (
            now,
            last_updated,
            delta_seconds,
            delta_seconds * 60 < OIDCSettings.get_profile_refresh_time(),
        )

    @staticmethod
    def requires_data_loading(user: settings.AUTH_USER_MODEL):
        if not user.last_updated:
            return True
        (
            now,
            last_updated,
            delta_seconds,
            requires_loading,
        ) = OIDCUserHelper._requires_loading(
            last_updated=user.last_updated,
            minutes_before_refresh=OIDCSettings.get_profile_refresh_time(),
        )

        if requires_loading:
            logger.debug(
                "User last refreshed: %s (%s) compared to now: %s (%s) is less than the refresh limit: %s minutes (delta: %s minutes) - No need to reload user data",
                last_updated,
                type(last_updated).__name__,
                now,
                type(now).__name__,
                OIDCSettings.get_profile_refresh_time(),
                delta_seconds,
            )
            return True
        return False

    @staticmethod
    def requires_group_loading(user: settings.AUTH_USER_MODEL):
        if not user.last_updated_groups:
            return True

        (
            now,
            last_updated,
            delta_seconds,
            requires_loading,
        ) = OIDCUserHelper._requires_loading(
            last_updated=user.last_updated_groups,
            minutes_before_refresh=OIDCSettings.get_profile_refresh_groups_time(),
        )

        if requires_loading:
            count = user.persisted_scouts_groups.count()
            if count > 0:
                logger.debug(
                    "User has persisted scouts groups (%d) and last refreshed: %s (%s) compared to now: %s (%s) is less than the refresh limit: %s minutes (delta: %s minutes) - No need to reload user groups",
                    count,
                    last_updated,
                    type(last_updated).__name__,
                    now,
                    type(now).__name__,
                    OIDCSettings.get_profile_refresh_groups_time(),
                    delta_seconds,
                )
                return True
        return False

    @staticmethod
    def requires_functions_loading(user: settings.AUTH_USER_MODEL):
        if not user.last_updated_functions:
            return True

        (
            now,
            last_updated,
            delta_seconds,
            requires_loading,
        ) = OIDCUserHelper._requires_loading(
            last_updated=user.last_updated_functions,
            minutes_before_refresh=OIDCSettings.get_profile_refresh_functions_time(),
        )

        if requires_loading:
            count = user.persisted_scouts_functions.count()
            if count > 0:
                logger.debug(
                    "User has persisted scouts functions (%d) and last refreshed: %s (%s) compared to now: %s (%s) is less than the refresh limit: %s minutes (delta: %s minutes) - No need to reload user groups",
                    count,
                    last_updated,
                    type(last_updated).__name__,
                    now,
                    type(now).__name__,
                    OIDCSettings.get_profile_refresh_functions_time(),
                    delta_seconds,
                )
                return True
        return False
