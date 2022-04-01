import os, json
from pathlib import Path
from typing import List

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.camps.models import CampYear, CampType
from apps.camps.services import CampYearService

from apps.visums.models import Category, CategoryPriority


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


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

        current_categories: List[Category] = Category.objects.all()
        loaded_categories: List[tuple] = []

        current_camp_year: CampYear = (
            CampYearService().get_or_create_current_camp_year()
        )

        default_camp_type: str = CampType.objects.get_default().camp_type
        all_camp_types: List[str] = [
            [camp_type.camp_type] for camp_type in CampType.objects.all().selectable()
        ]

        # Set to highest priority, since only Verbond will set categories for now
        # Highest priority: Verbond
        highest_priority = CategoryPriority.objects.get_highest_priority()

        previous_index = -1
        with open(path) as f:
            data = json.load(f)

            logger.debug("LOADING and REWRITING fixture %s", path)

            for model in data:
                # Allow ordering categories in the order in which they appear in the fixture json, without specifying the index
                previous_index = previous_index + 1
                model.get("fields")["index"] = previous_index

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

                # Allow creating categories for the current year without specifying the camp year
                if not "camp_year" in model.get("fields"):
                    model.get("fields")["camp_year"] = list()
                    model.get("fields")["camp_year"].append(current_camp_year.year)

                if not "priority" in model.get("fields"):
                    model.get("fields")["priority"] = list()
                    model.get("fields")["priority"].append(highest_priority.owner)

                loaded_categories.append(
                    (
                        model.get("fields").get("name"),
                        model.get("fields").get("camp_year")[0],
                    )
                )

                logger.trace("MODEL DATA: %s", model)

            with open(tmp_path, "w") as o:
                json.dump(data, o)

        logger.debug("LOADING adjusted fixture %s", tmp_path)
        call_command("loaddata", tmp_path)

        logger.debug("REMOVING adjusted fixture %s", tmp_path)
        os.remove(tmp_path)

        found_categories: List[Category] = []
        for name, camp_year in loaded_categories:
            for current_category in current_categories:
                if (
                    name == current_category.name
                    and camp_year == current_category.camp_year.year
                ):
                    found_categories.append(current_category)

        logger.debug(
            "FOUND categories: %d (%s)",
            len(found_categories),
            ", ".join(category.name for category in found_categories),
        )

        # linked_category_set_service = LinkedCategorySetService()
        for current_category in current_categories:
            if current_category not in found_categories:
                logger.debug(
                    "Removed category: %s (%s)",
                    current_category.name,
                    current_category.camp_year.year,
                )
                # linked_category_set_service.delete_category(
                #     request=None, category=current_category
                # )
                current_category.delete()
