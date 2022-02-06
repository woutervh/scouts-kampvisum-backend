import logging, os
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.camps.models import CampType
from apps.visums.models import CategorySetPriority, CategorySet, Category
from apps.visums.services import CampYearCategorySetService


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads the category sets from category_sets.json"
    exception = False

    BASE_PATH = "apps/visums/fixtures"
    FIXTURE = "category_sets.json"

    # def handle(self, *args, **kwargs):
    #     parent_path = Path(settings.BASE_DIR)
    #     data_path = "{}/{}".format(self.BASE_PATH, self.FIXTURE)
    #     path = os.path.join(parent_path, data_path)

    #     logger.debug("Loading category sets from %s", path)

    #     call_command("loaddata", path)
    def handle(self, *args, **kwargs):
        # Setup sets for all camp types, with highest priority
        camp_types = CampType.objects.all()
        # Verbond
        highest_priority = (
            CategorySetPriority.objects.all().order_by("priority").first()
        )
        # Current Camp Year
        camp_year_category_set = (
            CampYearCategorySetService().get_or_create_category_set_for_current_year()
        )

        for camp_type in camp_types:
            category_set = CategorySet.objects.get_by_camp_year_and_camp_type(
                camp_year=camp_year_category_set.camp_year, camp_type=camp_type
            )
            if not category_set:
                category_set = CategorySet()

                category_set.camp_year_category_set = camp_year_category_set
                category_set.camp_type = camp_type
                category_set.priority = highest_priority
            
            category_set.index = camp_type.index

            category_set.full_clean()
            category_set.save()

            categories = Category.objects.get_by_camp_type(camp_type)
            for category in categories:
                category_set.categories.add(category)
