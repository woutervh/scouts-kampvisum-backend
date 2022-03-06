from django.db import models


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineItemType(models.TextChoices):
    # alphabetically ordered
    DEADLINE = "D", "Deadline"
    LINKED_CHECK = "C", "LinkedCheck deadline"
    LINKED_SUB_CATEGORY = "S", "LinkedSubCategory deadline"

    def parse_deadline_type(value: str = None):
        if not value:
            return DeadlineItemType.DEADLINE

        value = value.upper()

        if value in ["D", "DEADLINE"]:
            return DeadlineItemType.DEADLINE
        if value in [
            "S",
            "SUB_CATEGORY",
            "SUBCATEGORY",
            "LINKED_SUB_CATEGORY",
            "LINKEDSUBCATEGORY",
        ]:
            return DeadlineItemType.LINKED_SUB_CATEGORY
        if value in ["C", "CHECK", "LINKED_CHECK", "LINKEDCHECK"]:
            return DeadlineItemType.LINKED_CHECK

        return DeadlineItemType.DEADLINE
