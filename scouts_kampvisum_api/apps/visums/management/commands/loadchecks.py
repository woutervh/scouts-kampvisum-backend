import os, json
from pathlib import Path
from typing import List

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.camps.models import CampType

from scouts_auth.inuits.utils import ListUtils


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the checks from checks.json"
    exception = False

    BASE_PATH = "apps/visums/fixtures"
    FIXTURE = "checks.json"
    TMP_FIXTURE = "{}_{}".format("adjusted", FIXTURE)

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        data_path = "{}/{}".format(self.BASE_PATH, self.FIXTURE)
        path = os.path.join(parent_path, data_path)

        tmp_data_path = "{}/{}".format(self.BASE_PATH, self.TMP_FIXTURE)
        tmp_path = os.path.join(parent_path, tmp_data_path)

        default_camp_type: str = CampType.objects.get_default().camp_type
        all_camp_types: List[str] = [
            [camp_type.camp_type] for camp_type in CampType.objects.all().selectable()
        ]

        logger.debug("Loading checks from %s", path)

        previous_sub_category = None
        previous_index = -1
        with open(path) as f:
            data = json.load(f)

            logger.debug("LOADING and REWRITING fixture %s", path)

            for model in data:
                # Allow ordering checks in the order in which they appear in the fixture json, without specifying the index
                sub_category = model.get("fields")["sub_category"]
                if previous_sub_category is None:
                    previous_sub_category = sub_category

                if previous_sub_category == sub_category:
                    previous_index = previous_index + 1
                else:
                    previous_sub_category = sub_category
                    previous_index = 0
                model.get("fields")["index"] = previous_index

                check_type = model.get("fields")["check_type"][0]
                if check_type in settings.ENFORCE_MEMBER_CHECKS:
                    model.get("fields")["is_member"] = True
                else:
                    model.get("fields")["is_member"] = False

                # If not present, set the default camp type
                camp_types: List[str] = model.get("fields").get("camp_types", [])
                results = []
                for camp_type in camp_types:
                    if isinstance(camp_type, str):
                        results.append(camp_type)
                    elif isinstance(camp_type, list) and isinstance(camp_type[0], str):
                        results.append(camp_type[0])
                camp_types = results
                if len(camp_types) == 0:
                    camp_types = [default_camp_type]
                # Check if the camp type is an expander (*)
                elif len(camp_types) == 1 and camp_types[0] == ["*"]:
                    camp_types = all_camp_types
                # Make sure that the default camp type is not present if other types are defined
                elif len(camp_types) > 1 and default_camp_type in camp_types:
                    camp_types.remove(default_camp_type)
                model.get("fields")["camp_types"] = [camp_types]

                logger.trace("MODEL DATA: %s", model)

            with open(tmp_path, "w") as o:
                json.dump(data, o)

        logger.debug("LOADING adjusted fixture %s", tmp_path)
        call_command("loaddata", tmp_path)

        logger.debug("REMOVING adjusted fixture %s", tmp_path)
        # os.remove(tmp_path)
