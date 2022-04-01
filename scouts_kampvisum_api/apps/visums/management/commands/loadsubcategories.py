import os, json
from pathlib import Path
from typing import List

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.camps.models import CampType

from apps.visums.models import SubCategory


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the categories from categories.json"
    exception = False

    BASE_PATH = "apps/visums/fixtures"
    FIXTURE = "sub_categories.json"
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

        logger.debug("Loading sub-categories from %s", path)

        current_sub_categories: List[SubCategory] = SubCategory.objects.all()
        loaded_sub_categories: List[tuple] = []

        previous_category = None
        previous_index = -1
        with open(path) as f:
            data = json.load(f)

            logger.debug("LOADING and REWRITING fixture %s", path)

            for model in data:
                # Allow ordering sub-categories in the order in which they appear in the fixture json, without specifying the index
                category = model.get("fields")["category"]
                if previous_category is None:
                    previous_category = category

                if previous_category == category:
                    previous_index = previous_index + 1
                else:
                    previous_category = category
                    previous_index = 0
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

                loaded_sub_categories.append(
                    (model.get("fields").get("name"), category)
                )

                logger.trace("MODEL DATA: %s", model)

            with open(tmp_path, "w") as o:
                json.dump(data, o)

        logger.debug("LOADING adjusted fixture %s", tmp_path)
        call_command("loaddata", tmp_path)

        logger.debug("REMOVING adjusted fixture %s", tmp_path)
        os.remove(tmp_path)

        found_sub_categories: List[SubCategory] = []
        for name, category in loaded_sub_categories:
            # logger.debug("LOADED SUB-CATEGORY: %s, %s", name, category)
            for current_sub_category in current_sub_categories:
                if (
                    name == current_sub_category.name
                    and category[0] == current_sub_category.category.name
                    and category[1] == current_sub_category.category.camp_year.year
                ):
                    found_sub_categories.append(current_sub_category)

        logger.debug(
            "FOUND sub-categories: %d (%s)",
            len(found_sub_categories),
            ", ".join(sub_category.name for sub_category in found_sub_categories),
        )

        for current_sub_category in current_sub_categories:
            if current_sub_category not in found_sub_categories:
                logger.debug(
                    "Removed sub-category: %s (%s [%s])",
                    current_sub_category.name,
                    current_sub_category.category.name,
                    current_sub_category.category.camp_year.year,
                )
                current_sub_category.delete()
