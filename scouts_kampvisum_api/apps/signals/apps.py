from django.apps import AppConfig


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SignalsConfig(AppConfig):
    name = "apps.signals"

    def ready(self):
        import scouts_auth.auth.signals
        from .signal_handler import SignalHandler

        logger.debug("App is ready")
