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
        # Do not attempt to refresh the session if the OIDC backend is not used
        is_oidc_enabled = True

        return (
            request.method == 'GET' and
            is_oidc_enabled and
            request.path not in self.exempt_urls and
            not any(pat.match(request.path)
                    for pat in self.exempt_url_patterns)
        )
