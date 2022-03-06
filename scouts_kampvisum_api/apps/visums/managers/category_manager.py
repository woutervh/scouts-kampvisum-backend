from django.db import models
from django.core.exceptions import ValidationError

from apps.camps.models import CampYear


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CategoryManager(models.Manager):
    """
    Loads Category instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db).order_by("index")

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        camp_year = kwargs.get("camp_year", None)
        camp_types = kwargs.get("camp_types", [])
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if camp_year and len(camp_types) > 0:
            try:
                return list(
                    self.get_queryset()
                    .filter(camp_year=camp_year, camp_types__in=camp_types)
                    .distinct()
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate Category instance(s) with provided params (id: {}, (camp_year: {}, camp_types: {})".format(
                    pk, camp_year, camp_types
                )
            )
        return None

    def get_by_natural_key(self, name, camp_year):
        logger.trace(
            "GET BY NATURAL KEY %s: (name: %s (%s), camp_year: %s (%s))",
            "Category",
            name,
            type(name).__name__,
            camp_year,
            type(camp_year).__name__,
        )

        if isinstance(camp_year, CampYear):
            return self.get(name=name, camp_year__year=camp_year.year)

        return self.get(name=name, camp_year__year=camp_year)
