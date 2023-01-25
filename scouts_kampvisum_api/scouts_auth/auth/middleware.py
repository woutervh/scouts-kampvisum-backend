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
        """Takes a request and returns whether it triggers a refresh examination

        :arg HttpRequest request:

        :returns: boolean

        """
        # This method call always returns false, because user.is_authenticated() always returns false
        # Seems to be a DRF problem, that should have been fixed, but clearly it's not
        # Results in the annoying 'request is not refreshable' message
        # See: https://github.com/mozilla/mozilla-django-oidc/issues/328
        #
        # The problem is that DRF instantiates an AnonymousUser that always returns false on
        # is_authenticated(). This should not happen, because
        """Takes a request and returns whether it triggers a refresh examination

        :arg HttpRequest request:

        :returns: boolean

        """
        logger.debug(f"REQUEST.USER type: {type(request.user).__name__}")
        logger.debug(f"REQUEST.USER: {request.user}")
        return super().is_refreshable_url(request)
