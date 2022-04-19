from django.db import models


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumApprovalState(models.TextChoices):
    """
    An enum that provides different visum approval states
    """

    # Base state, nothing to do yet
    UNDECIDED = "U", "UNDECIDED"
    # "OK": The visum category or sub-category is approved
    APPROVED = "A", "APPROVED"
    # "NOT OK": The visum category or sub-category is approved, but with remarks or conditions
    # Feedback will most likely be present in this state, but the camp can go ahead
    APPROVED_FEEDBACK = "N", "APPROVED_WITH_FEEDBACK"
    # "DISSAPPROVED": the visum does not pass the minimum guidelines and cannot be signed in this case
    DISAPPROVED = "D", "DISAPPROVED"

    @staticmethod
    def get_state(approval: str):
        approval = approval.lower()
        for option in CampVisumApprovalState.choices:
            if option[0].lower() == approval or option[1].lower() == approval:
                return option
        return CampVisumApprovalState.UNDECIDED
