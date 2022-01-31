import logging

from django.db import models

from apps.camps.models import CampYear

logger = logging.getLogger(__name__)


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

    def get_by_natural_key(self, name, camp_year):
        logger.debug(
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

    def get_by_camp_type(self, camp_type):
        return self.get_queryset().filter(camp_types__in=[camp_type])
