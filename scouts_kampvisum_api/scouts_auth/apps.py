from django.apps import AppConfig


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsAuthConfig(AppConfig):
    name = "scouts_auth"

    def ready(self):

        from .groupadmin.models import ScoutsUser
        from scouts_auth.auth.signals import ScoutsAuthSignalSender

        ScoutsAuthSignalSender().send_app_ready()
