import logging

from ..models import (
    LinkedCategory,
)
from ..services import CategoryService, CategorySetService, LinkedSubCategoryService
from apps.camps.models import Camp


logger = logging.getLogger(__name__)


class LinkedCategoryService:
    def link_category_set(self, camp: Camp):
        logger.debug("Linking categories to camp '%s'", camp.name)

        category_service = CategoryService()
        linked_sub_category_service = LinkedSubCategoryService()
        category_set = CategorySetService().get_default_set(camp.get_group_type())

        for category in category_set.categories.all():
            logger.debug("Linking category: '%s'", category.name)

            linked_category = LinkedCategory()

            linked_category.camp = camp
            linked_category.origin = category
            linked_category.category = category_service.deepcopy(category)

            linked_category.full_clean()
            linked_category.save()

            linked_sub_category_service.link_category(linked_category)

        return category_set
