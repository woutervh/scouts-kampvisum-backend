from scouts_auth.inuits.django import DjangoDbUtil

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PermissionHandler:

    @staticmethod
    def setup_roles(self):
        if not DjangoDbUtil._is_initial_db_ready():
            logger.debug(
                "Will not attempt to populate user permissions until migrations have been performed."
            )
            return

        try:
            # logger.debug("Populating user permissions")
            PermissionService().populate_roles()
        except Exception as exc:
            logger.error("Unable to populate user roles", exc)
