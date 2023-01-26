from django.core.management import call_command
from django.core.management.base import BaseCommand


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads all fixtures and runs all commands"
    exception = True

    COMMANDS = [
        "runfixtures",
        "setupcampyears",
        # "loadcategories",
        # "loadsubcategories",
        # "loadchecks",
        "loaddefaultdeadlines",
        # "fix92074",
        # "fix92074bis",
        # "sprint7fix91022",
        # "fix93032",
        # "fix92544tris",
        "updatevisums",
        "fix91782",
    ]

    def handle(self, *args, **kwargs):
        user = self.setup_admin_user()

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

    def setup_admin_user(self, *args, **kwargs):
        from scouts_auth.groupadmin.models import ScoutsUser

        username = "FIXTURES"

        user = ScoutsUser.objects.safe_get(username=username)

        if user:
            return user

        user = ScoutsUser()

        user.username = username
        user.password = username
        user.group_admin_id = username

        user.full_clean()
        user.save()

        return user