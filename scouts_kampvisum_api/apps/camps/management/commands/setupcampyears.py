import os
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sets up the camp years"
    exception = False

    BASE_PATH = "apps/camps/fixtures"
    FIXTURE = "camp_years.json"

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        data_path = "{}/{}".format(self.BASE_PATH, self.FIXTURE)
        path = os.path.join(parent_path, data_path)

        logger.debug("LOADING camp year fixture %s", path)
        call_command("loaddata", path) 

        from apps.camps.services import CampYearService

        logger.debug("Setting up camp years")
        CampYearService().setup_camp_years()
