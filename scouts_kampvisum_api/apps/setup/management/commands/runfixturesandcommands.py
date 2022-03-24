from django.core.management import call_command
from django.core.management.base import BaseCommand


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads all fixtures and runs all commands"
    exception = False

    COMMANDS = [
        "runfixtures",
        "setupcampyears",
        "loadcategories",
        "loadsubcategories",
        "loadchecks",
        "loaddefaultdeadlines",
        "fix92074",
        "fix92074bis",
        "sprint7fix91022",
    ]

    def handle(self, *args, **kwargs):
        for command in self.COMMANDS:
            logger.debug(
                "==========================================================================="
            )
            logger.debug("RUNNING COMMAND %s", command)
            logger.debug(
                "==========================================================================="
            )
            call_command(command)
            logger.debug("")
            logger.debug("")
            logger.debug("")
