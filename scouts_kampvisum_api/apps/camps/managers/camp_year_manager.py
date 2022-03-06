from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampYearQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CampYearManager(models.Manager):
    """
    Loads CampYear instances by their integer year, not their id/uuid.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CampYearQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        year = kwargs.get("year", None)
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if year:
            try:
                return self.get_queryset().get(year=year)
            except:
                pass

        if start_date and end_date:
            try:
                return self.get_queryset().get(start_date=start_date, end_date=end_date)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate CampType instance with provided params (id: {}, year: {}, start_date: {}, end_date: {})".format(
                    pk, year, start_date, end_date
                )
            )
        return None

    def get_by_natural_key(self, year):
        logger.trace(
            "GET BY NATURAL KEY %s: (year: %s (%s))",
            "CampYear",
            year,
            type(year).__name__,
        )
        return self.get(year=year)
