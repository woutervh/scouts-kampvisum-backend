from django.db import transaction

from apps.camps.services import CampTypeService

from apps.visums.models import (
    CampVisum,
    LinkedCategorySet,
)
from apps.visums.services import CategoryService


import logging

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
        linked_category_set = LinkedCategorySet()

        linked_category_set.visum = visum

        linked_category_set.full_clean()
        linked_category_set.save()

        return self.category_service.create_linked_categories(
            request=request,
            linked_category_set=linked_category_set,
        )

    @transaction.atomic
    def update_linked_category_set(
        self,
        request,
        instance: LinkedCategorySet,
        visum: CampVisum,
    ) -> LinkedCategorySet:
        return self.category_service.update_linked_categories(
            request=request,
            linked_category_set=instance,
        )
