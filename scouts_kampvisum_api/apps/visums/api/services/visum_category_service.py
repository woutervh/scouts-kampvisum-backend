import logging

from ..models import (
    CampVisumLinkedCategory,
)
from ..services import CampVisumCategoryService, CampVisumCategorySetService
from apps.camps.models import Camp


logger = logging.getLogger(__name__)


class CampVisumLinkedCategoryService():

    def link_category_set(self, camp: Camp):
        logger.debug("Linking categories to camp '%s'", camp.name)

        category_service = CampVisumCategoryService()
        category_set = CampVisumCategorySetService().get_default_set(
            camp.get_group_type()
        )

        for category in category_set.categories.all():
            logger.debug("Linked category: '%s'", category.name)

            linked_category = CampVisumLinkedCategory()

            linked_category.camp = camp
            linked_category.origin = category
            linked_category.category = category_service.deepcopy(category)

            linked_category.full_clean()
            linked_category.save()

            # for sub_category in category:
            #     linked_sub_category = CampVisumLinkedSubCategory()

            #     linked_sub_category
