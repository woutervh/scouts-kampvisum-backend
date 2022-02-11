import logging, os, json
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.deadlines.models import DeadlineDate
from apps.deadlines.services import DeadlineDateService


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the default deadlines from default_deadlines.json"
    exception = False

    BASE_PATH = "apps/deadlines/fixtures"
    FIXTURE = "default_deadlines.json"
    TMP_FIXTURE = "{}_{}".format("adjusted", FIXTURE)

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        data_path = "{}/{}".format(self.BASE_PATH, self.FIXTURE)
        path = os.path.join(parent_path, data_path)

        tmp_data_path = "{}/{}".format(self.BASE_PATH, self.TMP_FIXTURE)
        tmp_path = os.path.join(parent_path, tmp_data_path)

        logger.debug("Loading default deadlines from %s", path)

        date_service = DeadlineDateService()

        with open(path) as f:
            data = json.load(f)

            for model in data:
                due_date: DeadlineDate = date_service.create_deadline_date(
                    None, **model.get("fields")["due_date"]
                )
                model.get("fields")["due_date"] = str(due_date.id)

                logger.debug("MODEL: %s", model)

            with open(tmp_path, "w") as o:
                json.dump(data, o)

        call_command("loaddata", tmp_path)

        os.remove(tmp_path)
