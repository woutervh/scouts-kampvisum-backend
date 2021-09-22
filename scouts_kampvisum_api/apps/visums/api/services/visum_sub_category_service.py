import logging

from ..models import LinkedCategory, LinkedSubCategory
from ..services import SubCategoryService, LinkedConcernService


logger = logging.getLogger(__name__)


class LinkedSubCategoryService:
    def link_category(self, category: LinkedCategory):
        logger.debug("Linking sub categories to category '%s'", category.category.name)

        sub_category_service = SubCategoryService()
        linked_concern_service = LinkedConcernService()

        for sub_category in category.category.sub_categories.all():
            logger.debug("Linking sub category: '%s'", sub_category.name)

            linked_sub_category = LinkedSubCategory()

            linked_sub_category.category = category
            linked_sub_category.origin = sub_category
            linked_sub_category.sub_category = sub_category_service.deepcopy(
                sub_category
            )

            linked_sub_category.full_clean()
            linked_sub_category.save()

            linked_concern_service.link_sub_category(linked_sub_category)
