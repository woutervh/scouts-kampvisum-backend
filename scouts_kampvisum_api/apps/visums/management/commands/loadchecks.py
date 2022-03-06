import os, json
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


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

                logger.trace("MODEL DATA: %s", model)

            with open(tmp_path, "w") as o:
                json.dump(data, o)

        logger.debug("LOADING adjusted fixture %s", tmp_path)
        call_command("loaddata", tmp_path)

        logger.debug("REMOVING adjusted fixture %s", tmp_path)
        os.remove(tmp_path)
