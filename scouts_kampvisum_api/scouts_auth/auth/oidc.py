from types import SimpleNamespace
from typing import Tuple
from requests.exceptions import HTTPError

from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.utils import timezone

from rest_framework import exceptions

from scouts_auth.auth.models import User


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    pass


class InuitsOIDCAuthentication(OIDCAuthentication):
    def get_user(self, request):
        logger.debug("EREH EREH EREH")

    def authenticate(self, request) -> Tuple:
        """ "
        Call parent authenticate but catch HTTPError 401 always,
        even without www-authenticate.
        """
        try:
            logger.debug(
                "OIDC AUTHENTICATION: Authenticating user with OIDC backend")

            result = super().authenticate(request)

            if result is None:
                logger.error(
                    "SCOUTS-AUTH: Authentication failed, refresh required")

                return None

            if isinstance(result, tuple):
                (user, token) = result

                user.last_authenticated = timezone.now()
                user.full_clean()
                user.save()

                return (user, token)
        except HTTPError as exc:
            logging.exception(
                "SCOUTS-AUTH: Authentication error: %s", exc.response.json()
            )

            response = exc.response
            # If oidc returns 401 return auth failed error
            if response.status_code == 401:
                logging.error("SCOUTS-AUTH: 401 Unable to authenticate")

                raise exceptions.AuthenticationFailed(
                    response.json().get("error_description", response.text)
                )

            raise

        return None
