from types import SimpleNamespace
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from mozilla_django_oidc.auth import OIDCAuthenticationBackend


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    pass
