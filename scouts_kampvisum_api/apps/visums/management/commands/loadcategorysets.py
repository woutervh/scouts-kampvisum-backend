import logging, os
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the category sets from visum_category_sets.json"
    exception = False

    BASE_PATH = "apps/visums/fixtures"
    FIXTURE = "visum_category_sets.json"

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)
        data_path = "{}/{}".format(self.BASE_PATH, self.FIXTURE)
        path = os.path.join(parent_path, data_path)

        logger.debug("Loading category sets from %s", path)

        call_command("loaddata", path)
