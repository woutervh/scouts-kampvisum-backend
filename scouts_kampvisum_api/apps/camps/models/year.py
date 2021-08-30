from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..managers import CampYearManager
from apps.base.models import BaseModel


class CampYear(BaseModel):
    """
    Represents a scouts year.

    A camp year starts on the 1st of September and ends on the 31st of August
    of the next calendar year, but will be displayed as the next calendar year
    (the year that the camp will actually take place).
    e.g. the displayed year for a CampYear that starts on 01/09/2021 is 2022
    """

    year = models.IntegerField(_("year"))
    start_date = models.DateField()
    end_date = models.DateField()

    objects = CampYearManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year'], name='unique_year')
        ]

    def natural_key(self):
        return (self.year, )

    def __str__(self):
        return "CampYear {self.year}: {self.start_date} - {self.end_date}".format(self=self)
