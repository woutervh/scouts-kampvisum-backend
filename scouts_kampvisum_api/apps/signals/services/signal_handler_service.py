from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from scouts_auth.auth.signals import (
    ScoutsAuthSignalSender,
    app_ready,
)
from scouts_auth.auth.services import PermissionService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SignalHandlerService:

    handling_login = False
    handling_refresh = False
    handling_authentication = False

    @staticmethod
    @receiver(
        app_ready,
        sender=ScoutsAuthSignalSender.sender,
        dispatch_uid=ScoutsAuthSignalSender.app_ready_uid,
    )
    def handle_app_ready(*args, **kwargs):
        signal = "app_ready"
        logger.debug(
            "SIGNAL received: '%s' from %s", signal, ScoutsAuthSignalSender.sender
        )
        if not SignalHandlerService._is_initial_db_ready():
            logger.debug(
                "Will not attempt to populate user permissions until migrations have been performed."
            )
            return

        try:
            # logger.debug("Populating user permissions")
            PermissionService().populate_roles()
        except Exception as exc:
            logger.error("Unable to populate user roles", exc)

    @staticmethod
    def _is_initial_db_ready() -> bool:
        try:
            content_type = ContentType.objects.last()

            if content_type:
                return True
        except:
            logger.debug(
                "Unable to load authentication groups, database is probably not ready yet"
            )

        return False
