import os, json
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.camps.models import CampYear
from apps.camps.services import CampYearService, CampTypeService

from apps.deadlines.models import Deadline, DeadlineItem, DeadlineDate
from apps.deadlines.services import (
    DeadlineService,
    DeadlineItemService,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the deadlines from deadlines.json"
    exception = False

    BASE_PATH = "apps/deadlines/fixtures"
    FIXTURES = ["deadlines.json", "camp_registration_deadlines.json"]

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        for FIXTURE in self.FIXTURES:
            TMP_FIXTURE = "{}_{}".format("adjusted", FIXTURE)

            data_path = "{}/{}".format(self.BASE_PATH, FIXTURE)
            path = os.path.join(parent_path, data_path)

            tmp_data_path = "{}/{}".format(self.BASE_PATH, TMP_FIXTURE)
            tmp_path = os.path.join(parent_path, tmp_data_path)

            logger.debug("Loading deadlines from %s", path)

            deadline_service = DeadlineService()
            deadline_item_service = DeadlineItemService()
            camp_year_service = CampYearService()
            camp_type_service = CampTypeService()

            current_camp_year: CampYear = (
                camp_year_service.get_or_create_current_camp_year()
            )

            previous_index = -1
            with open(path) as f:
                data = json.load(f)

                logger.debug("LOADING and REWRITING fixture %s", path)

                for model in data:
                    previous_index = previous_index + 1
                    model["index"] = previous_index

                    # Allow creating deadlines for the current year without specifying the camp year
                    if not "camp_year" in model.get("fields"):
                        model.get("fields")["camp_year"] = list()
                        model.get("fields")["camp_year"].append(current_camp_year.year)

                    if not "camp_types" in model.get("fields"):
                        model.get("fields")["camp_types"] = list()
                    else:
                        camp_types = model.get("fields")["camp_types"]

                        model.get("fields")["camp_types"] = list()

                        for camp_type in camp_types:
                            model.get("fields")["camp_types"].append([camp_type])

                    camp_types = camp_type_service.get_camp_types(
                        camp_types=[
                            camp_type[0]
                            for camp_type in model.get("fields")["camp_types"]
                        ],
                        include_default=False,
                    )

                    deadline: Deadline = deadline_service.get_or_create_deadline(
                        request=None,
                        name=model.get("fields")["name"],
                        camp_year=current_camp_year,
                        camp_types=camp_types,
                        items=[],
                    )
                    model["pk"] = str(deadline.id)

                    due_date: DeadlineDate = (
                        deadline_service.get_or_create_deadline_date(
                            deadline=deadline, **model.get("fields")["due_date"]
                        )
                    )
                    model.get("fields").pop("due_date")

                    items = model.get("fields").get("items", [])
                    if len(items) == 0:
                        raise ValidationError(
                            "No DeadlineItem instances defined to link to Deadline !"
                        )

                    previous_item_index = -1
                    if items:
                        if len(items) == 0:
                            raise ValidationError("A deadline needs items")

                        for item in items:
                            # Allow ordering categories in the order in which they appear in the fixture json, without specifying the index
                            previous_item_index = previous_item_index + 1
                            item["index"] = previous_item_index

                            logger.debug("item: %s", item)
                            deadline_item: DeadlineItem = (
                                deadline_item_service.create_or_update_deadline_item(
                                    request=None, deadline=deadline, **item
                                )
                            )
                    model.get("fields").pop("items")

                    logger.trace("MODEL: %s", model)

                with open(tmp_path, "w") as o:
                    json.dump(data, o)

            logger.debug("LOADING adjusted fixture %s", tmp_path)
            call_command("loaddata", tmp_path)

            logger.debug("REMOVING adjusted fixture %s", tmp_path)
            os.remove(tmp_path)
