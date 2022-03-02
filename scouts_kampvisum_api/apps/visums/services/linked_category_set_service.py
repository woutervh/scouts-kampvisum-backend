import logging
from typing import List

from django.db import transaction

from apps.camps.models import Camp, CampYear, CampType
from apps.camps.services import CampTypeService

from apps.visums.models import (
    CampVisum,
    Category,
    LinkedCategorySet,
)
from apps.visums.services import CategoryService


logger = logging.getLogger(__name__)


class LinkedCategorySetService:
    """
    Service for managing category sets.
    """

    camp_type_service = CampTypeService()
    category_service = CategoryService()

    @transaction.atomic
    def create_linked_category_set(
        self, request, visum: CampVisum
    ) -> LinkedCategorySet:
        camp_year: CampYear = visum.camp.year
        categories: List[Category] = self.category_service.get_categories(
            camp_year=camp_year, camp_types=visum.camp_types.all()
        )
        logger.debug(
            "Found %d Category instances for camp_year %d and camp_types %s",
            len(categories),
            camp_year.year,
            ",".join(camp_type.camp_type for camp_type in visum.camp_types.all()),
        )

        linked_category_set = LinkedCategorySet()

        linked_category_set.visum = visum

        linked_category_set.full_clean()
        linked_category_set.save()

        return self.category_service.link_categories(
            request, linked_category_set, categories
        )

    @transaction.atomic
    def update_linked_category_set(
        self,
        request,
        instance: LinkedCategorySet,
        camp: Camp,
        camp_types: List[CampType],
    ) -> LinkedCategorySet:
        camp_year: CampYear = camp.year
        categories: List[Category] = self.category_service.get_categories(
            camp_year=camp_year, camp_types=camp_types
        )
        logger.debug(
            "Found %d Category instances for camp_year %d and camp_types %s",
            len(categories),
            camp_year.year,
            camp_types,
        )

        linked_category_set = LinkedCategorySet()

        linked_category_set.camp_types = camp_types

        linked_category_set.full_clean()
        linked_category_set.save()

        return self.category_service.link_categories(
            request, linked_category_set, categories
        )
