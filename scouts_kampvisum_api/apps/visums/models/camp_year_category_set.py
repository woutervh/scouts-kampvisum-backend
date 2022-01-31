import logging

from django.db import models

from apps.camps.models import CampYear
from apps.visums.managers import CampYearCategorySetManager

from scouts_auth.inuits.models import AbstractBaseModel


logger = logging.getLogger(__name__)


class CampYearCategorySet(AbstractBaseModel):

    objects = CampYearCategorySetManager()

    camp_year = models.ForeignKey(
        CampYear, on_delete=models.CASCADE, related_name="camp_year_category_set"
    )

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED CampYearCategorySet")
        return (self.camp_year.year,)

    def __str__(self):
        return "OBJECT CampYearCategorySet: camp_year({})".format(str(self.camp_year))
