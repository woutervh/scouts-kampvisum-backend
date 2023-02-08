from typing import Tuple
from requests.exceptions import HTTPError

from mozilla_django_oidc.contrib.drf import OIDCAuthentication

from django.utils import timezone

from rest_framework import exceptions

from scouts_auth.auth.exceptions import ScoutsAuthException


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsOIDCAuthentication(OIDCAuthentication):

    def authenticate(self, request) -> Tuple:
        """ "
        Call parent authenticate but catch HTTPError 401 always,
        even without www-authenticate.
        """
        try:
            logger.debug(
                "OIDC AUTHENTICATION: Authenticating user with OIDC backend")

            # This calls get_or_create_user() in ScoutsOIDCAuthenticationBackend
            result = super().authenticate(request)

            if result is None:
                return None

            if isinstance(result, tuple):
                (user, token) = result

                now = timezone.now()

                user.last_authenticated = now
                user.updated_on = now

                user.full_clean()
                user.save()

                return (user, token)
        except HTTPError as exc:
            logging.error(
                "SCOUTS-AUTH: Authentication error: %s", exc.response.json()
            )

            response = exc.response
            # If oidc returns 401 return auth failed error
            if response.status_code == 401:
                raise ScoutsAuthException(
                    "SCOUTS-AUTH: 401 Unable to authenticate: " +
                    response.json().get("error_description", response.text)
                )

            raise
