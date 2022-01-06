from django.db import models


class CheckState(models.TextChoices):
    UNCHECKED = "", "Unchecked"
    CHECKED = "", "Checked"
    IRRELEVANT = "", "Irrelevant"
