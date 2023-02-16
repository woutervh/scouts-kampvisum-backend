from django.core.management import call_command
from django.core.management.base import BaseCommand

from scouts_auth.auth.services import PermissionService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads all fixtures and runs all commands"
    exception = True

    permission_service = PermissionService()

    def handle(self, *args, **kwargs):
        self.permission_service.setup_permission_groups()
