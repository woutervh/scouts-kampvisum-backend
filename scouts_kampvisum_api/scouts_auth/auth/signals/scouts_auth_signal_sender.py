from django.conf import settings

from . import app_ready, oidc_login, oidc_refresh, oidc_authenticated


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
        # logger.debug("SCOUTS-AUTH: Sending SIGNAL 'app_ready'")
        app_ready.send(sender=self.sender)

    def send_oidc_login(self, user: settings.AUTH_USER_MODEL):
        # logger.debug("SCOUTS-AUTH: Sending SIGNAL 'login'")
        oidc_login.send(sender=self.sender, user=user)

    def send_oidc_refresh(self, user: settings.AUTH_USER_MODEL):
        # logger.debug("SCOUTS-AUTH: Sending SIGNAL 'refreshed'")
        oidc_refresh.send(sender=self.sender, user=user)

    def send_oidc_authenticated(self, user: settings.AUTH_USER_MODEL):
        # logger.debug("SCOUTS-AUTH: Sending SIGNAL 'authenticated'")
        oidc_authenticated.send(sender=self.sender, user=user)
