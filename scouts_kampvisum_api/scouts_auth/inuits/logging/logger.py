from logging import Logger

from django.conf import settings


class InuitsLogger(Logger):
    name: str
    level: str

    def __init__(self, name, level=None):
        self.name = name
        self.level = level if level else settings.LOGGING_LEVEL

        super().__init__(name=self.name, level=self.level)

    def debug(self, msg, *args, **kwargs):
        super().debug(self, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        super().info(self, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        super().warning(self, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        super().error(self, msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        super().exception(self, msg, *args, exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        super().critical(self, msg, *args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        print("TRACE", msg if not isinstance(msg, object) else str(msg), *args, **kwargs)
