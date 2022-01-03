import logging


from apps.visums.models import (
    CampYearCategorySet,
    CategorySet,
    Category,
    CategorySetPriority,
)
from apps.camps.models import CampYear
from apps.camps.services import CampYearService
from apps.groups.models import ScoutsGroupType


logger = logging.getLogger(__name__)


class CategorySetService:
    """
    Service for managing category sets.
    """

    # def setup_default_set(
    #     self,
    #     category_set: CampYearCategorySet,
    #     group_type: ScoutsGroupType,
    #     categories,
    #     priority: CategorySetPriority,
    # ) -> CategorySet:
    #     # Setup default category set
    #     category_set = CategorySet()
    #     category_set.category_set = category_set
    #     category_set.group_type = group_type
    #     category_set.priority = priority

    #     category_set.full_clean()
    #     category_set.save()

    #     for category in categories:
    #         category_set.categories.add(category)

    #     category_set.full_clean()
    #     category_set.save()

    #     return category_set

    # def setup_default_sets(self):
    #     """
    #     Sets up a default category set.
    #     """
    #     # Get highest priority for default set
    #     priority = CategorySetPriority.objects.earliest("priority")
    #     # Types
    #     types = ScoutsGroupType.objects.filter(parent=None)
    #     # Get current CampYear
    #     year = CampYearService().get_or_create_year()
    #     # Default categories
    #     categories = Category.objects.filter(is_default=True)

    #     # Setup default category set for all group types
    #     for type in types:
    #         if not self.has_default_set(type):
    #             logger.debug("No existing category set found for type '%s'", type.type)
    #             return [self.setup_default_set(type, year, categories, priority)]
    #         else:
    #             logger.debug(
    #                 "Not setting up category set for type '%s', it already exists",
    #                 type.type,
    #             )

    #     return []
