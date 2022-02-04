from django.db import models


class CheckState(models.TextChoices):
    EMPTY = "EMPTY", "Empty"
    UNCHECKED = "UNCHECKED", "Unchecked"
    CHECKED = "CHECKED", "Checked"
    NOT_APPLICABLE = "NOT_APPLICABLE", "Not applicable"
