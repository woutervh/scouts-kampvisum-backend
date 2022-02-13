import logging

from django.db import models


logger = logging.getLogger(__name__)


class DeadlineType(models.TextChoices):
    # alphabetically ordered
    DEADLINE = "D", "Deadline"
    LINKED_CHECK = "C", "LinkedCheck deadline"
    LINKED_SUB_CATEGORY = "S", "LinkedSubCategory deadline"
    MIXED = "M", "Mix of linked checks and sub categories deadline"

    def parse_deadline_type(value: str = None):
        if not value:
            return DeadlineType.DEADLINE

        value = value.upper()

        if value in ["D", "DEADLINE"]:
            return DeadlineType.DEADLINE
        if value in [
            "S",
            "SUB_CATEGORY",
            "SUBCATEGORY",
            "LINKED_SUB_CATEGORY",
            "LINKEDSUBCATEGORY",
        ]:
            return DeadlineType.LINKED_SUB_CATEGORY
        if value in ["C", "CHECK", "LINKED_CHECK", "LINKEDCHECK"]:
            return DeadlineType.LINKED_CHECK
        if value in ["M", "MIXED"]:
            return DeadlineType.MIXED

        return DeadlineType.DEADLINE
