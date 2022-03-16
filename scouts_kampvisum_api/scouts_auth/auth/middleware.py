import jwt

from django.contrib.auth import BACKEND_SESSION_KEY
from django.utils.module_loading import import_string

from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.middleware import SessionRefresh

from scouts_auth.groupadmin.models import ScoutsUser


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsAuthSessionRefresh(SessionRefresh):
    def is_refreshable_url(self, request):
        # Do not attempt to refresh the session if the OIDC backend is not used
        # backend_session = request.session.get(BACKEND_SESSION_KEY)
        # is_oidc_enabled = True
        # if backend_session:
        #     auth_backend = import_string(backend_session)
        #     is_oidc_enabled = issubclass(auth_backend, OIDCAuthenticationBackend)

        # logger.debug("request: %s (%s)", request.user, type(request.user).__name__)
        # # logger.debug("request: %s", dir(request))
        # # logger.debug(
        # #     "request headers: %s", request.headers
        # # )  # logger.debug("request access token: %s", request.access_token)
        # # logger.debug("auth: %s", request.headers.get("Authorization"))

        # logger.debug("request.method = 'GET' -> %s", request.method == "GET")
        # logger.debug(
        #     "request.user.is_authenticated -> %s", request.user.is_authenticated
        # )
        # logger.debug("is_oidc_enable -> %s", is_oidc_enabled)

        # auth = request.headers.get("Authorization", None)

        # if auth:
        #     access_token = auth.split(" ")[1]
        #     decoded = jwt.decode(
        #         access_token,
        #         algorithms=["RS256"],
        #         verify=False,
        #         options={"verify_signature": False},
        #     )
        #     username = decoded.get("preferred_username", None)
        #     logger.debug("USERNAME: %s", username)

        #     if username:
        #         logger.debug("SETTING USERNAME on request")
        #         user = ScoutsUser.objects.safe_get(username=username)

        #         request.user = user
        #         request._force_auth_user = user
        #         # request._force_auth_token = Token.objects.get(user=user)
        #         request._force_auth_token = access_token

        is_refreshable = super().is_refreshable_url(request)

        # logger.debug("request: %s (%s)", request.user, type(request.user).__name__)
        # logger.debug("request.method = 'GET' -> %s", request.method == "GET")
        # logger.debug(
        #     "request.user.is_authenticated -> %s", request.user.is_authenticated
        # )
        # logger.debug("is_oidc_enable -> %s", is_oidc_enabled)

        return is_refreshable
