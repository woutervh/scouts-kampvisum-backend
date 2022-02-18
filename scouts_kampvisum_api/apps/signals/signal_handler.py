import logging

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.dispatch import receiver

from apps.groups.services import ScoutsSectionService

from scouts_auth.auth.signals import (
    ScoutsAuthSignalSender,
    app_ready,
    authenticated,
    refreshed,
)
from scouts_auth.auth.services import PermissionService
from scouts_auth.auth.user import OIDCUserHelper

from scouts_auth.groupadmin.services import ScoutsAuthorizationService


logger = logging.getLogger(__name__)


class SignalHandler:
    @staticmethod
    @receiver(
        app_ready,
        sender=ScoutsAuthSignalSender.sender,
        dispatch_uid=ScoutsAuthSignalSender.app_ready_uid,
    )
    def handle_app_ready(**kwargs):
        logger.debug(
            "SIGNAL received: 'app_ready' from %s", ScoutsAuthSignalSender.sender
        )
        if not SignalHandler._is_initial_db_ready():
            logger.debug(
                "Will not attempt to populate user permissions until migrations have been performed."
            )
            return

        try:
            logger.debug("Populating user permissions")
            PermissionService().populate_roles()
        except Exception as exc:
            logger.error("Unable to populate user roles", exc)

    @staticmethod
    @receiver(
        authenticated,
        sender=ScoutsAuthSignalSender.sender,
        dispatch_uid=ScoutsAuthSignalSender.authenticated_uid,
    )
    def handle_authenticated(
        user: settings.AUTH_USER_MODEL, **kwargs
    ) -> settings.AUTH_USER_MODEL:
        """
        Reads additional data for a user and takes appropriate action.

        Some user data necessary for permissions can only be loaded by a groupadmin profile call after authentication.
        This method handles a signal for the basic oidc authentication, then makes the necessary additional calls.
        """
        logger.debug(
            "SIGNAL received: 'authenticated' from %s", ScoutsAuthSignalSender.sender
        )
        logger.debug("AUTHENTICATED USER: %s (%s)", user.username, type(user).__name__)

        authorization_service = ScoutsAuthorizationService()
        section_service = ScoutsSectionService()

        if OIDCUserHelper.requires_data_loading(user=user):
            logger.debug
            logger.debug(
                "SIGNAL handling for 'authenticated' -> Loading additional user groups"
            )
            user = authorization_service.load_user_scouts_groups(user)

            logger.debug(
                "SIGNAL handling for 'authenticated' -> Loading scouts functions"
            )
            user = authorization_service.load_user_functions(user)

            logger.debug(
                "SIGNAL handling for 'authenticated' -> Setting up sections for user's groups"
            )
            section_service.setup_default_sections(user=user)

        logger.debug(user.to_descriptive_string())

        return user

    @staticmethod
    @receiver(
        refreshed,
        sender=ScoutsAuthSignalSender.sender,
        dispatch_uid=ScoutsAuthSignalSender.refreshed_uid,
    )
    def handle_refreshed(user: settings.AUTH_USER_MODEL, **kwargs):
        logger.debug(
            "SIGNAL received: 'refreshed' from %s", ScoutsAuthSignalSender.sender
        )
        logger.debug("REFRESHED USER: %s (%s)", user.username, type(user).__name__)

    @staticmethod
    def _is_initial_db_ready() -> bool:
        try:
            content_types = ContentType.objects.all()

            if content_types:
                return True
        except:
            logger.debug(
                "Unable to load authentication groups, database is probably not ready yet"
            )

        return False
