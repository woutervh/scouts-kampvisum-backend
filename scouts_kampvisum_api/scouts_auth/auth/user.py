import logging
import datetime

from django.conf import settings


logger = logging.getLogger(__name__)


class OIDCUserHelper:
    @staticmethod
    def requires_data_loading(user: settings.AUTH_USER_MODEL):
        # @TODO implement ?
        return True
