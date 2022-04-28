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
    # "FEEDBACK_RESOLVED": the necessary steps were taking to resolve the issue in feedback (state was DISAPPROVED)
    FEEDBACK_RESOLVED = "F", "FEEDBACK_RESOLVED"
    # "FEEDBACK_READ": the leaders have acknowledged the DC's remarks (state was APPROVED_FEEDBACK)
    FEEDBACK_READ = "R", "FEEDBACK_READ"

    @staticmethod
    def get_state(approval: str):
        approval = approval.lower()
        for option in CampVisumApprovalState.choices:
            if option[0].lower() == approval or option[1].lower() == approval:
                return option
        return CampVisumApprovalState.UNDECIDED

    def get_state_enum(approval: any):
        if isinstance(approval, CampVisumApprovalState):
            return approval

        states = [
            CampVisumApprovalState.UNDECIDED,
            CampVisumApprovalState.APPROVED,
            CampVisumApprovalState.APPROVED_FEEDBACK,
            CampVisumApprovalState.DISAPPROVED,
            CampVisumApprovalState.FEEDBACK_RESOLVED,
            CampVisumApprovalState.FEEDBACK_READ,
        ]

        if isinstance(approval, tuple):
            for state in states:
                if approval[0] == state or approval[1] == state.label:
                    return state

        if isinstance(approval, str):
            for state in states:
                if approval == state or approval == state.label:
                    return state

        return CampVisumApprovalState.UNDECIDED
