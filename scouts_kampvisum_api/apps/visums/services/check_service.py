from typing import List

from django.db import transaction

from apps.visums.models import (
    LinkedSubCategory,
    SubCategory,
    Check,
    LinkedCheck,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckService:
    @transaction.atomic
    def link_checks(
        self, request, linked_sub_category: LinkedSubCategory, sub_category: SubCategory
    ) -> LinkedSubCategory:
        checks: List[Check] = Check.objects.safe_get(
            sub_category=sub_category,
            camp_types=linked_sub_category.category.category_set.visum.camp_types.all(),
            raise_error=True,
        )

        logger.debug(
            "Linking %d checks to sub-category %s (%s)",
            len(checks),
            linked_sub_category.id,
            linked_sub_category.parent.name,
        )

        for check in checks:
            self.link_check(
                request=request,
                linked_sub_category=linked_sub_category,
                check=check,
            )

        return linked_sub_category

    @transaction.atomic
    def link_check(
        self, request, linked_sub_category: LinkedSubCategory, check: Check
    ) -> LinkedCheck:
        linked_check = LinkedCheck.get_concrete_check_type(check)

        logger.debug(
            "Linked check: %s (type: %s)", check.name, type(linked_check).__name__
        )

        linked_check.parent = check
        linked_check.sub_category = linked_sub_category

        linked_check.full_clean()
        linked_check.save()

        return linked_check
