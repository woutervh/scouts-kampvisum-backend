from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.groups.models import ScoutsSection
from apps.groups.services import ScoutsSectionService

from scouts_auth.auth.oidc_user_helper import OIDCUserHelper

from scouts_auth.groupadmin.services import (
    ScoutsUserService,
    ScoutsAuthorizationService,
)

from scouts_auth.inuits.cache import InuitsCache

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsScoutsUserService(ScoutsUserService):

    section_serviec = ScoutsSectionService()

    def _check_user_data(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:

        super()._check_user_data(user=user)

        try:
            self.section_service.setup_default_sections(user=user)
        except Exception as exc:
            raise ValidationError(
                "An error occured while setting up default scouts sections", exc
            )
