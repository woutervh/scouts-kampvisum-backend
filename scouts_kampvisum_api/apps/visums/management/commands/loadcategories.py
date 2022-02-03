import logging, os, json
from pathlib import Path
from typing import List

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.camps.models import CampYear, CampType
from apps.camps.services import CampYearService


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the categories from categories.json"
    exception = False

    BASE_PATH = "apps/visums/fixtures"
    FIXTURE = "categories.json"
    TMP_FIXTURE = "{}_{}".format("adjusted", FIXTURE)

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        data_path = "{}/{}".format(self.BASE_PATH, self.FIXTURE)
        path = os.path.join(parent_path, data_path)

        tmp_data_path = "{}/{}".format(self.BASE_PATH, self.TMP_FIXTURE)
        tmp_path = os.path.join(parent_path, tmp_data_path)

        logger.debug("Loading categories from %s", path)

        current_camp_year: CampYear = (
            CampYearService().get_or_create_current_camp_year()
        )
        all_camp_types = [[camp_type.camp_type] for camp_type in CampType.objects.all()]

        previous_index = -1
        with open(path) as f:
            data = json.load(f)

            for model in data:
                # Allow ordering categories in the order in which they appear in the fixture json
                previous_index = previous_index + 1
                model.get("fields")["index"] = previous_index

                # Check if the camp type is an expander (*)
                camp_types: list = model.get("fields")["camp_types"]
                if len(camp_types) == 0 or (
                    len(camp_types) == 1 and camp_types[0] == ["*"]
                ):
                    model.get("fields")["camp_types"] = all_camp_types

                # Allow creating categories for the current year without specifying the camp year
                if not "camp_year" in model.get("fields"):
                    model.get("fields")["camp_year"] = list()
                    model.get("fields")["camp_year"].append(current_camp_year.year)

                logger.debug("MODEL DATA: %s", model)

            with open(tmp_path, "w") as o:
                json.dump(data, o)

        call_command("loaddata", tmp_path)

        os.remove(tmp_path)
