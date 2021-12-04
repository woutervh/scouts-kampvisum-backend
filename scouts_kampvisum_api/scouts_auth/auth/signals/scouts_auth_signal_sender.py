import logging

from django.conf import settings

from . import app_ready, authenticated


logger = logging.getLogger(__name__)


class ScoutsAuthSignalSender:
    sender = "scouts-auth"

    app_ready_uid = "scouts_auth__app_ready"
    authenticated_uid = "scouts_auth__authenticated"

    def send_app_ready(self):
        logger.debug("SCOUTS-AUTH: Sending SIGNAL 'app_ready'")
        app_ready.send(sender=self.sender)

    def send_authenticated(self, user: settings.AUTH_USER_MODEL):
        logger.debug("SCOUTS-AUTH: Sending SIGNAL 'authenticated'")
        authenticated.send(sender=self.sender, user=user)
