import logging

from apps.camps.models import Camp, CampYear
from apps.camps.services import CampYearService
from apps.groups.models import ScoutsGroupType
from apps.visums.models import (
    CampType,
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
        self, request, camp_year: CampYear, camp_type: CampType = None
    ) -> CategorySet:
        if camp_type is None:
            logger.warn("No camp type given, getting default CampType instance")
            camp_type = CampType.objects.get_default()

        logger.debug(
            "Looking for category sets for camp year %s and camp type %s",
            camp_year.to_simple_str(),
            camp_type.camp_type,
        )
        qs = CategorySet.objects.filter(
            camp_year_category_set__camp_year=camp_year, camp_type=camp_type
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
        category_set = self.get_default_category_set(request, camp_year=camp.year)

        linked_category_set = LinkedCategorySet()

        linked_category_set.parent = category_set

        linked_category_set.full_clean()
        linked_category_set.save()

        return self.category_service.link_categories(
            request, linked_category_set, category_set
        )
