import logging, copy

from apps.visums.models import LinkedSubCategory, SubCategory, LinkedCheck, Check


logger = logging.getLogger(__name__)


class CheckService:
    def link_checks(
        self, linked_sub_category: LinkedSubCategory, sub_category: SubCategory
    ) -> LinkedSubCategory:
        logger.debug("Linking checks")

        for check in sub_category.checks.all():
            logger.debug("Linked check: %s", check.name)
            linked_check = LinkedCheck()

            linked_check.parent = check
            linked_check.sub_category = linked_sub_category

            linked_check.full_clean()
            linked_check.save()

        return linked_sub_category
