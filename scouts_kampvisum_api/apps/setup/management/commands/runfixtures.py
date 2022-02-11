import logging, os, json
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.deadlines.models import DeadlineDate
from apps.deadlines.services import DeadlineDateService


logger = logging.getLogger(__name__)

# FIXTURES=(
# 	"scouts_group_types.json"
# 	"scouts_section_names.json"
# 	"default_scouts_section_names.json"
# 	"camp_types.json"
# 	"category_set_priorities.json"
# 	"check_types.json"
# )
class Command(BaseCommand):
    help = "Loads all fixtures"
    exception = False

    BASE_PATH = "apps/"

    FIXTURES = [
        "groups/fixtures/scouts_group_types.json",
        "groups/fixtures/scouts_section_names.json",
        "groups/fixtures/default_scouts_section_names.json",
        "camps/fixtures/camp_types.json",
        "visums/fixtures/category_set_priorities.json",
        "visums/fixtures/check_types.json",
    ]

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        for fixture in self.FIXTURES:
            data_path = "{}/{}".format(self.BASE_PATH, fixture)
            path = os.path.join(parent_path, data_path)

            call_command("loaddata", path)
