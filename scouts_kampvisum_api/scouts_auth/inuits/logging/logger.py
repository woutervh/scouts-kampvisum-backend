import logging
import logging.config
from logging import Logger

from django.conf import settings
from django.utils import timezone


class InuitsLogger(Logger):
    name: str
    level: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # super().setLevel(settings.LOGGING_LEVEL)

    def _pass_log(self, level, msg, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            msg = "[{}] {}".format(user.username, msg)

        self.log(level, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._pass_log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._pass_log(logging.ERROR, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._pass_log(logging.INFO, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._pass_log(logging.DEBUG, msg, *args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        self._pass_log(logging.TRACE, msg, *args, **kwargs)

    def note(self, msg, *args, **kwargs):
        self._pass_log(logging.NOTE, msg, *args, **kwargs)

    def api(self, msg, *args, **kwargs):
        self._pass_log(logging.API, msg, *args, **kwargs)

    def timing(self, start: timezone, user: settings.AUTH_USER_MODEL, endpoint: str = '', method: str = 'GET', function: str = None, breakpoint: str = None):
        self._pass_log(
            logging.DEBUG, f"[TIMING] {(timezone.now() - start).total_seconds()}{(' ' + method + ' ' + endpoint) if endpoint else ''}{(' ' + breakpoint) if breakpoint else ''}{(' ' + function) if function else ''}", user=user)

    @staticmethod
    def setup_logging(level='DEBUG', config=None):
        logging.NOTE = logging.INFO + 5
        logging.TRACE = logging.DEBUG - 5
        logging.API = logging.DEBUG - 10

        logging.addLevelName(logging.INFO + 5, "NOTE")
        logging.addLevelName(logging.DEBUG - 5, "TRACE")
        logging.addLevelName(logging.DEBUG - 10, "API")

        logging.setLoggerClass(InuitsLogger)

        if config:
            logging.config.dictConfig(config)
