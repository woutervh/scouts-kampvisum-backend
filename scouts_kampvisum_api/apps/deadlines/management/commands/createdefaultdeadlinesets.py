import logging, os, json
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.deadlines.models import DefaultDeadline, DeadlineDate
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.services import DefaultDeadlineService


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the default deadline sets from default_deadline_sets.json"
    exception = False

    BASE_PATH = "apps/deadlines/fixtures"
    FIXTURE = "default_deadline_sets.json"

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        data_path = "{}/{}".format(self.BASE_PATH, self.FIXTURE)
        path = os.path.join(parent_path, data_path)

        call_command("loaddata", path)
