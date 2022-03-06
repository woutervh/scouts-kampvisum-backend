from django.conf import settings

from . import app_ready, authenticated, refreshed


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsAuthSignalSender:
    sender = "scouts-auth"

    app_ready_uid = "scouts_auth__app_ready"
    authenticated_uid = "scouts_auth__authenticated"
    refreshed_uid = "scouts_auth__refreshed"

    def send_app_ready(self):
        logger.debug("SCOUTS-AUTH: Sending SIGNAL 'app_ready'")
        app_ready.send(sender=self.sender)

    def send_authenticated(self, user: settings.AUTH_USER_MODEL):
        logger.debug("SCOUTS-AUTH: Sending SIGNAL 'authenticated'")
        authenticated.send(sender=self.sender, user=user)

    def send_refreshed(self, user: settings.AUTH_USER_MODEL):
        logger.debug("SCOUTS-AUTH: Sending SIGNAL 'refreshed'")
        refreshed.send(sender=self.sender, user=user)
