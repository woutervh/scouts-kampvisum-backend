import logging

from django.db import models


logger = logging.getLogger(__name__)


class Gender(models.TextChoices):
    # alphabetically ordered
    FEMALE = "F", "Female"
    MIXED = "I", "Mixed"
    MALE = "M", "Male"
    OTHER = "O", "Other"
    UNKNOWN = "U", "Unknown"


class GenderHelper:
    @staticmethod
    def parse_gender(value: str = None) -> Gender:
        if not value:
            return Gender.UNKNOWN

        value = value.strip().upper()
        if value in ["F", "FEMALE", "V", "VROUW"]:
            return Gender.FEMALE
        # Used in specifying a group that can consist of heterogenous genders
        if value in ["I", "MIXED", "GEMENGD", "ALLERLEI"]:
            return Gender.MIXED
        if value in ["M", "MALE", "MAN"]:
            return Gender.MALE
        if value in ["O", "OTHER", "A", "ANDER", "ANDERE"]:
            return Gender.OTHER

        return Gender.UNKNOWN
