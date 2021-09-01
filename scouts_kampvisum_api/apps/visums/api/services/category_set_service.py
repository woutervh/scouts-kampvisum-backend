import logging


from ..models import (
    CategorySet,
    Category,
    CategorySetPriority,
)
from apps.camps.services import CampYearService
from apps.groups.api.models import GroupType


logger = logging.getLogger(__name__)


class CategorySetService:
    """
    Service for managing category sets.
    """

    def get_default_set(self, type: GroupType) -> CategorySet:
        logger.debug("Looking for default category sets for type '%s'", type)
        return CategorySet.objects.get(is_default=True, type=type)

    def setup_default(self, category_set: CategorySet = None):
        """
        Sets up a default category set.
        """

        # Get highest priority for default set
        priority = CategorySetPriority.objects.earliest('priority')
        # Types
        types = GroupType.objects.filter(parent=None)
        # Get current CampYear
        year = CampYearService().get_or_create_year()
        # Default categories
        categories = Category.objects.filter(is_default=True)

        if category_set is None:
            # Setup default category set for all group types
            for group_type in types:
                # Setup default category set
                category_set = CategorySet()
                category_set.priority = priority
                category_set.type = group_type
                category_set.camp_year = year
                category_set.is_default = True
                category_set.full_clean()
                category_set.save()

                for category in categories:
                    category_set.categories.add(category)

                category_set.full_clean()
                category_set.save()
