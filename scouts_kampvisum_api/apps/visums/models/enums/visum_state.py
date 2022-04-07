from django.db import models


class CampVisumState(models.TextChoices):
    """
    An enum that descibes the state of a CampVisum (with regards to the DC approval flow)
    """

    # CampVisum is new or doesn't yet have all required data filled in
    # FRONTEND: "Kamp goedkeuren" -> button disabled
    DATA_REQUIRED = "DATA_REQUIRED", "data_required"
    # CampVisum has all required data, leaders and group leaders can sign the engagement
    # FRONTEND: "Kamp goedkeuren" -> button enabled
    SIGNABLE = "SIGNABLE", "signable"
    # CampVisum has been signed by leaders and group leaders, DC can start approval flow
    REVIEWABLE = "REVIEWABLE", "reviewable"
    # DC has approved the camp visum
    REVIEWED_APPROVED = "REVIEWED_APPROVED", "reviewed_approved"
    # DC has approved the camp visum, but added feedback for some categories/sub-categories
    REVIEWED_FEEDBACK = "REVIEWED_FEEDBACK", "reviewed_feedback"
    # DC has disapproved the camp visum, action by leaders and group leaders required
    REVIEWED_DISAPPROVED = "REVIEWED_DISAPPROVED", "reviewed_disapproved"
    # CampVisum was disapproved, leaders/group leaders have revisited the failed items
    FEEDBACK_HANDLED = "FEEDBACK_HANDLED", "feedback_handled"

    @staticmethod
    def endpoint_from_type(check_type: str):
        for option in CampVisumState.choices:
            if option[0] == check_type:
                return option[1]
        return None
