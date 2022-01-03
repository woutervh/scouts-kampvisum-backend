import logging

from django.db import models


logger = logging.getLogger(__name__)


class CampYearCategorySetManager(models.Manager):
    def get_by_natural_key(self, camp_year):
        logger.debug(
            "GET BY NATURAL KEY %s: (camp_year: %s (%s))",
            "CampYearCategorySet",
            camp_year,
            type(camp_year).__name__,
        )
        return self.get(camp_year__year=camp_year)
