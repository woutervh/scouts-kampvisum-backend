from http.client import OK
from django.db import models


class ApprovalStateEnum(models.TextChoices):
    """
    An enum that provides differente visum approval states
    """

    UNDECIDED = "U", "UNDECIDED"
    # "OK": The visum category or sub-category is approved
    APPROVED = "A", "APPROVED"
    # "NOT OK": The visum category or sub-category is approved, but with remarks or conditions
    # Feedback will most likely be present in this state, but the camp can go ahead
    NOT_APPROVED = "N", "NOT_APPROVED"
    # "DISSAPPROVED": the visum does not pass the minimum guidelines and cannot be signed in this case
    DISAPPROVED = "D", "DISAPPROVED"

    @staticmethod
    def endpoint_from_type(check_type: str):
        for option in ApprovalStateEnum.choices:
            if option[0] == check_type:
                return option[1]
        return None
