import logging

from apps.visums.models import (
    LinkedSubCategory,
    SubCategory,
    LinkedCheck,
)


logger = logging.getLogger(__name__)


class VisumCheckService:
    def link_checks(
        self, request, linked_sub_category: LinkedSubCategory, sub_category: SubCategory
    ) -> LinkedSubCategory:
        logger.debug("Linking checks")

        for check in sub_category.checks.all():
            linked_check = LinkedCheck.get_concrete_check_type(check)
            logger.debug(
                "Linked check: %s (type: %s)", check.name, type(linked_check).__name__
            )

            linked_check.parent = check
            linked_check.sub_category = linked_sub_category

            linked_check.full_clean()
            linked_check.save()

        return linked_sub_category
