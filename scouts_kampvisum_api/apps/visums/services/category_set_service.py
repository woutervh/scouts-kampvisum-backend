import logging

from apps.camps.models import Camp, CampYear
from apps.camps.services import CampYearService
from apps.groups.models import ScoutsGroupType
from apps.visums.models import (
    CampYearCategorySet,
    CategorySet,
    Category,
    CategorySetPriority,
    LinkedCategorySet,
)
from apps.visums.services import CampYearCategorySetService, CategoryService

from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class CategorySetService:
    """
    Service for managing category sets.
    """

    camp_year_category_set_service = CampYearCategorySetService()
    category_service = CategoryService()
    group_admin = GroupAdmin()

    def get_default_category_set(
        self, request, camp_year: CampYear, group_type: ScoutsGroupType
    ) -> CategorySet:
        logger.debug(
            "Looking for category sets for camp year %s and group type %s",
            camp_year.to_simple_str(),
            group_type.to_simple_str(),
        )
        qs = CategorySet.objects.filter(
            category_set__camp_year=camp_year, group_type=group_type
        )

        if qs.count() > 0:
            return qs[0]

        return None

    def has_default_set(self, request, type: ScoutsGroupType):
        category_set = self.get_default_set(request, type)

        if category_set is not None:
            return True

        return False

    def get_linked_category_set(self, request, camp: Camp) -> LinkedCategorySet:
        category_set = self.get_default_category_set(
            request, camp_year=camp.year, group_type=camp.sections.first().group_type
        )

        linked_category_set = LinkedCategorySet()

        linked_category_set.parent = category_set

        linked_category_set.full_clean()
        linked_category_set.save()

        return self.category_service.link_categories(
            request, linked_category_set, category_set
        )

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
