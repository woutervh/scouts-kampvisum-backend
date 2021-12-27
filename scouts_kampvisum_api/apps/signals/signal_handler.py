import logging

from django.conf import settings
from django.dispatch import receiver

from scouts_auth.auth.signals import ScoutsAuthSignalSender, app_ready, authenticated
from scouts_auth.auth.services import PermissionService

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
        try:
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

        service = ScoutsAuthorizationService()

        if not user.fully_loaded:
            logger.debug(
                "SIGNAL handling for 'authenticated' -> Loading additional user groups"
            )
            user = service.load_user_scouts_groups(user)
            logger.debug(
                "SIGNAL handling for 'authenticated' -> Loading scouts functions"
            )
            user = service.load_user_functions(user)
        user.fully_loaded = True

        logger.debug(user.to_descriptive_string())

        return user
