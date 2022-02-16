import logging
from typing import List

from apps.camps.models import Camp, CampYear, CampType

from apps.groups.models import ScoutsGroupType

from apps.visums.models import (
    CategorySet,
    LinkedCategorySet,
)
from apps.visums.services import CampYearCategorySetService, CategoryService

from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.inuits.utils import ListUtils


logger = logging.getLogger(__name__)


class CategorySetService:
    """
    Service for managing category sets.
    """

    camp_year_category_set_service = CampYearCategorySetService()
    category_service = CategoryService()
    group_admin = GroupAdmin()

    def get_default_category_set(
        self, request, camp_year: CampYear, camp_types: List[str] = None
    ) -> CategorySet:
        default_camp_type = [CampType.objects.get_default()]

        if camp_types is None or len(camp_types) == 0:
            logger.warn("No camp type given, getting default CampType instance")
            camp_types = default_camp_type
        else:
            camp_types = ListUtils.concatenate_unique_lists(
                default_camp_type,
                [CampType.objects.get(name=name) for name in camp_types],
            )

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

    def has_default_set(self, request, type: ScoutsGroupType):
        category_set = self.get_default_set(request, type)

        if category_set is not None:
            return True

        return False

    def get_linked_category_set(
        self, request, camp_types: List[str], camp: Camp
    ) -> LinkedCategorySet:
        category_set = self.get_default_category_set(
            request=request, camp_types=camp_types, camp_year=camp.year
        )

        linked_category_set = LinkedCategorySet()

        linked_category_set.parent = category_set

        linked_category_set.full_clean()
        linked_category_set.save()

        return self.category_service.link_categories(
            request, linked_category_set, category_set
        )
