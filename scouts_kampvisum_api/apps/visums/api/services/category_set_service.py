import logging


from ..models import (
    CampVisumCategorySet,
    CampVisumCategory,
    CampVisumSubCategory,
    CampVisumConcern,
    CampVisumLinkedCategory,
    CampVisumLinkedSubCategory,
    CampVisumLinkedConcern,
    CampVisumCategorySetPriority,
)
from apps.camps.models import Camp
from apps.camps.services import CampYearService
from apps.groups.api.models import GroupType


logger = logging.getLogger(__name__)


class CampVisumCategorySetService:
    """
    Convenience service for creating default category sets.
    """

    def setup(self, category_set: CampVisumCategorySet = None):
        """
        Links default categories to a camp.
        """

        # Get highest priority for default set
        priority = CampVisumCategorySetPriority.objects.earliest('priority')
        # Types
        types = GroupType.objects.filter(parent=None)
        # Get current CampYear
        year = CampYearService().get_or_create_year()
        # Default categories
        categories = CampVisumCategory.objects.filter(is_default=True)

        if category_set is None:
            # Setup default category set for all group types
            for group_type in types:
                # Setup default category set
                category_set = CampVisumCategorySet()
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

        # for category in categories:
        #     sub_categories = category.sub_categories
        #     for sub_category in sub_categories:
        # linked_sub_category = self.save_linked_sub_category(
        #     CampVisumLinkedSubCategory(linked_category)
        # )

        # checks = sub_category.checks
        # for check in checks:
        #     linked_check = CampVisumLinkedConcern()
        #     linked_sub_category.checks.add(linked_check)
        # linked_category.sub_categories.add(linked_sub_category)

    def save_linked_category(
        self, category: CampVisumLinkedCategory
    ) -> CampVisumLinkedCategory:
        category.full_clean()
        category.save()

        return category

    def save_linked_sub_category(
        self, sub_category: CampVisumLinkedSubCategory
    ) -> CampVisumLinkedSubCategory:

        sub_category.full_clean()
        sub_category.save()

        return sub_category

    def save_linked_check(self, check: CampVisumLinkedConcern) -> CampVisumLinkedConcern:
        check.full_clean()
        check.save()

        return check
