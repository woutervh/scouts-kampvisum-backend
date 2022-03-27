from django.conf import settings

from scouts_auth.auth.settings import OIDCSettings
from scouts_auth.groupadmin.services import GroupAdmin


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class OIDCService:

    oidc_endpoint = OIDCSettings.get_oidc_op_token_endpoint()
    oidc_rp_client_id = OIDCSettings.get_oidc_rp_client_id()
    oidc_rp_client_secret = OIDCSettings.get_oidc_rp_client_secret()

    service = GroupAdmin()

    def get_tokens_by_auth_code(self, auth_code: str, redirect_uri: str) -> dict:
        payload = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "client_id": self.oidc_rp_client_id,
            "client_secret": self.oidc_rp_client_secret,
            "redirect_uri": redirect_uri,
        }
        logger.debug("SCOUTS_AUTH: OIDC - sending authentication token")

        return self.service.post(self.oidc_endpoint, payload)

    def get_tokens_by_refresh_token(
        self, user: settings.AUTH_USER_MODEL, refresh_token: str
    ) -> dict:
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": self.oidc_rp_client_id,
            "client_secret": self.oidc_rp_client_secret,
        }
        logger.debug("SCOUTS_AUTH: OIDC - refreshing authentication")

        result = self.service.post(self.oidc_endpoint, payload)

        # ScoutsAuthSignalSender().send_oidc_refresh(user=user)

        return result
