from django.conf import settings


import logging

logger = logging.getLogger(__name__)


class OIDCUserHelper:
    @staticmethod
    def requires_data_loading(user: settings.AUTH_USER_MODEL):
        # @TODO implement ?
        return True
