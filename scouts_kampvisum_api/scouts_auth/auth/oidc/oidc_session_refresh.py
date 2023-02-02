from mozilla_django_oidc.middleware import SessionRefresh


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsOIDCSessionRefresh(SessionRefresh):

    def is_refreshable_url(self, request):
        """Takes a request and returns whether it triggers a refresh examination

        :arg HttpRequest request:

        :returns: boolean

        """
        # This method call always returns False, because user.is_authenticated() always returns False.
        # Seems to be a DRF problem, that should have been fixed, but clearly it's not
        # Results in the annoying 'request is not refreshable' message and the subsequent authorisation calls (on per GET).
        # See: https://github.com/mozilla/mozilla-django-oidc/issues/328
        #
        # The problem is that DRF instantiates an AnonymousUser that always returns false on
        # is_authenticated().
        logger.debug(
            f"REQUEST.USER type: {type(request.user).__name__}", user=request.user)
        logger.debug(f"REQUEST.USER: {request.user}", user=request.user)

        return super().is_refreshable_url(request)
