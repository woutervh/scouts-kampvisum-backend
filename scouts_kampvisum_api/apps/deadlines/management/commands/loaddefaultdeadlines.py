import logging, os, json
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.deadlines.models import DeadlineDate
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.services import DefaultDeadlineService


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the default deadlines from default_deadlines.json"
    exception = False

    BASE_PATH = "apps/deadlines/fixtures"
    FIXTURES = ["default_deadlines.json", "camp_registration_deadlines.json"]

    def handle(self, *args, **kwargs):
        parent_path = Path(settings.BASE_DIR)

        for FIXTURE in self.FIXTURES:
            TMP_FIXTURE = "{}_{}".format("adjusted", FIXTURE)

            data_path = "{}/{}".format(self.BASE_PATH, FIXTURE)
            path = os.path.join(parent_path, data_path)

            tmp_data_path = "{}/{}".format(self.BASE_PATH, TMP_FIXTURE)
            tmp_path = os.path.join(parent_path, tmp_data_path)

            logger.debug("Loading default deadlines from %s", path)

            default_deadline_service = DefaultDeadlineService()

            with open(path) as f:
                data = json.load(f)

                for model in data:
                    default_deadline = default_deadline_service.get_or_create(
                        name=model.get("fields")["name"],
                        deadline_type=model.get("fields").get(
                            "deadline_type", DeadlineType.DEADLINE
                        ),
                    )
                    model["pk"] = str(default_deadline.id)

                    due_date: DeadlineDate = (
                        default_deadline_service.get_or_create_deadline_date(
                            default_deadline=default_deadline,
                            **model.get("fields")["due_date"]
                        )
                    )
                    # model.get("fields")["due_date"] = [str(default_deadline.id)]
                    model.get("fields").pop("due_date")

                    flags = model.get("fields").get("flags", [])
                    if flags:
                        results = []

                        for flag in flags:
                            name = flag[0]
                            label = flag[1] if flag[1] else None

                            results.append(
                                default_deadline_service.get_or_create_default_flag(
                                    default_deadline=default_deadline,
                                    **{
                                        "name": name,
                                        "label": label,
                                    }
                                )
                            )

                        # model.get("fields")["flags"] = [str(flag.id) for flag in results]
                        model.get("fields").pop("flags")

                    # logger.debug("MODEL: %s", model)

                with open(tmp_path, "w") as o:
                    json.dump(data, o)

            call_command("loaddata", tmp_path)

            os.remove(tmp_path)
