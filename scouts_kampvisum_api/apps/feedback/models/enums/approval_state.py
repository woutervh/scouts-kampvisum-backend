from django.db import models


class ApprovalState(models.TextChoices):

    APPROVED = "APPROVED", "approved"
    APPROVED_FEEDBACK = "APPROVED_FEEDBACK", "approved_with_feedback"
    DISAPPROVED = "DISAPPROVED", "disapproved"
