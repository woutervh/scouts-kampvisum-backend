import logging

from ..models import LinkedSubCategory, LinkedConcern
from ..services import ConcernService


logger = logging.getLogger(__name__)


class LinkedConcernService:
    def link_sub_category(self, sub_category: LinkedSubCategory):
        logger.debug(
            "Linking concerns to sub-category '%s'", sub_category.sub_category.name
        )

        concern_service = ConcernService()

        for concern in sub_category.origin.concerns.all():
            logger.debug("Linking concern: '%s'", concern.name)

            linked_concern = LinkedConcern()

            linked_concern.sub_category = sub_category
            linked_concern.origin = concern
            linked_concern.concern = concern_service.deepcopy(concern)

            linked_concern.full_clean()
            linked_concern.save()

        return
