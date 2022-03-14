from typing import List

from django.db import transaction

from apps.camps.models import CampType

from apps.visums.models import (
    CampVisum,
    LinkedCategorySet,
)
from apps.visums.services import LinkedCategoryService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCategorySetService:
    """
    Service for managing category sets.
    """

    linked_category_service = LinkedCategoryService()

    @transaction.atomic
    def create_linked_category_set(
        self, request, visum: CampVisum
    ) -> LinkedCategorySet:
        linked_category_set = LinkedCategorySet()

        linked_category_set.visum = visum

        linked_category_set.full_clean()
        linked_category_set.save()

        return self.linked_category_service.create_linked_categories(
            request=request,
            linked_category_set=linked_category_set,
        )

    @transaction.atomic
    def update_linked_category_set(
        self,
        request,
        instance: LinkedCategorySet,
        visum: CampVisum,
        current_camp_types: List[CampType] = None,
    ) -> LinkedCategorySet:
        return self.linked_category_service.update_linked_categories(
            request=request,
            linked_category_set=instance,
            current_camp_types=current_camp_types,
        )
