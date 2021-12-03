import logging

from ..models import LinkedCategorySet
from ..services import LinkedCategoryService
from apps.camps.models import Camp


logger = logging.getLogger(__name__)


class LinkedCategorySetService:
    """
    Service for managing category sets.
    """

    def category_set_create(self, camp: Camp) -> LinkedCategorySet:
        logger.debug("Linking category set to camp %s", camp.name)

        category_set = LinkedCategoryService().link_category_set(camp)
        linked_category_set = LinkedCategorySet()

        linked_category_set.origin = category_set

        linked_category_set.full_clean()
        linked_category_set.save()

        return linked_category_set
