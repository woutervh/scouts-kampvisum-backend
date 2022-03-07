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
    def requires_data_loading(user: settings.AUTH_USER_MODEL):
        # @TODO implement ?
        return True

    @staticmethod
    def requires_group_loading(user: settings.AUTH_USER_MODEL):
        now: timezone.datetime = timezone.now()
        last_refreshed: datetime = user.last_refreshed
        
        delta_seconds = int(now.timestamp()) - int(last_refreshed.timestamp())
        
        if delta_seconds * 60 < OIDCSettings.get_profile_refresh_groups_time():
            if user.persisted_scouts_groups.count() > 0:
                logger.debug("User has persisted scouts groups (%d) and last refreshed: %s (%s) compared to now: %s (%s) is less than the refresh limit: %s minutes (delta: %s minutes) - No need to reload user groups", user.persisted_scouts_groups.count(), last_refreshed, type(last_refreshed).__name__, now, type(now).__name__, OIDCSettings.get_profile_refresh_time(), delta_seconds)
                return False

        return True
