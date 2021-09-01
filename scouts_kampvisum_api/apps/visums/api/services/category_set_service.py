import logging


from ..models import (
    CategorySet,
    Category,
    CategorySetPriority,
)
from apps.camps.models import CampYear
from apps.camps.services import CampYearService
from apps.groups.api.models import GroupType


logger = logging.getLogger(__name__)


class CategorySetService:
    """
    Service for managing category sets.
    """

    def get_default_set(self, type: GroupType) -> CategorySet:
        logger.debug("Looking for default category sets for type '%s'", type.type)
        qs = CategorySet.objects.filter(is_default=True, type=type)

        if qs.count() > 0:
            return qs[0]

        return None

    def has_default_set(self, type: GroupType):
        category_set = self.get_default_set(type)

        if category_set is not None:
            return True

        return False

    def setup_default_set(
        self, type: GroupType, year: CampYear, categories, priority: CategorySetPriority
    ) -> CategorySet:
        # Setup default category set
        category_set = CategorySet()
        category_set.priority = priority
        category_set.type = type
        category_set.camp_year = year
        category_set.is_default = True
        category_set.full_clean()
        category_set.save()

        for category in categories:
            category_set.categories.add(category)

        category_set.full_clean()
        category_set.save()

    def setup_default_sets(self):
        """
        Sets up a default category set.
        """
        # Get highest priority for default set
        priority = CategorySetPriority.objects.earliest("priority")
        # Types
        types = GroupType.objects.filter(parent=None)
        # Get current CampYear
        year = CampYearService().get_or_create_year()
        # Default categories
        categories = Category.objects.filter(is_default=True)

        # Setup default category set for all group types
        for type in types:
            if not self.has_default_set(type):
                logger.debug("No existing category set found for type '%s'", type.type)
                self.setup_default_set(type, year, categories, priority)
            else:
                logger.debug(
                    "Not setting up category set for type '%s',\
                         it already exists",
                    type.type,
                )
