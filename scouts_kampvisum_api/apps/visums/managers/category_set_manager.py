import logging

from django.db import models


logger = logging.getLogger(__name__)


class CategorySetQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CategorySetManager(models.Manager):
    """
    Loads CategorySet instances by their camp year category set, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CategorySetQuerySet(self.model, using=self._db).order_by(
            "priority__priority"
        )

    def get_by_natural_key(self, category_set):
        logger.debug(
            "GET BY NATURAL KEY %s: (category_set: %s (%s)",
            "CategorySet",
            category_set,
            type(category_set).__name__,
        )

        return self.get(category_set__camp_year__year=category_set)

    def get_by_camp_year_and_camp_type(self, camp_year, camp_type):
        logger.debug(
            "Querying for CategorySet with camp year %s and camp type %s",
            camp_year.year,
            camp_type.camp_type,
        )
        try:
            return self.get_queryset().get(
                camp_year_category_set__camp_year=camp_year, camp_type=camp_type
            )
        except:
            return None
