import logging

from django.db import models


logger = logging.getLogger(__name__)


class DeadlineType(models.TextChoices):
    # alphabetically ordered
    DEADLINE = "D", "Deadline"
    CHECK = "C", "Check deadline"
    SUB_CATEGORY = "S", "SubCategory deadline"
    
    def parse_deadline_type(value: str = None):
        if not value:
            return DeadlineType.DEADLINE
        
        if value in ["D", "DEADLINE"]:
            return DeadlineType.DEADLINE
        if value in ["C", "CHECK"]:
            return DeadlineType.CHECK
        if value in ["S", "SUB_CATEGORY"]:
            return DeadlineType.SUB_CATEGORY
        
        return DeadlineType.DEADLINE