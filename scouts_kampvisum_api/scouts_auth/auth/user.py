from django.conf import settings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class OIDCUserHelper:
    @staticmethod
    def requires_data_loading(user: settings.AUTH_USER_MODEL):
        # @TODO implement ?
        return True
