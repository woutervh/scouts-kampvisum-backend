import logging
from typing import List

from apps.camps.models import Camp, CampYear, CampType
from apps.camps.services import CampTypeService

from apps.groups.models import ScoutsGroupType

from apps.visums.models import (
    CategorySet,
    LinkedCategorySet,
)
from apps.visums.services import CampYearCategorySetService, CategoryService

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class CategorySetService:
    """
    Service for managing category sets.
    """

    camp_year_category_set_service = CampYearCategorySetService()
    category_service = CategoryService()
    group_admin = GroupAdmin()
    camp_type_service = CampTypeService()

    def create_category_set(
        self, request, camp_year: CampYear, camp_types: List[CampType]
    ) -> CategorySet:

        logger.debug(
            "Looking for category sets for camp year %s and camp types %s",
            camp_year.to_simple_str(),
            ",".join(instance.camp_type for instance in camp_types),
        )
        qs = CategorySet.objects.filter(
            camp_year_category_set__camp_year=camp_year, camp_type__in=camp_types
        )

        if qs.count() > 0:
            return qs[0]

        return None

    def create_linked_category_set(
        self, request, camp_types: List[str], camp: Camp
    ) -> LinkedCategorySet:
        camp_types: List[CampType] = self.camp_type_service.load_camp_types(
            camp_types=camp_types
        )
        category_set = self.create_category_set(
            request=request, camp_types=camp_types, camp_year=camp.year
        )

        linked_category_set = LinkedCategorySet()

        linked_category_set.parent = category_set

        linked_category_set.full_clean()
        linked_category_set.save()

        return self.category_service.link_categories(
            request, linked_category_set, category_set
        )
