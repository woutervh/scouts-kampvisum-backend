import logging

from django.db import models


logger = logging.getLogger(__name__)


class SubCategoryManager(models.Manager):
    """
    Loads Category instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name, category):
        # logger.debug(
        #     "GET BY NATURAL KEY %s: (name: %s (%s), camp_year: %s (%s), group_type: %s (%s))",
        #     "SubCategory",
        #     name,
        #     type(name).__name__,
        #     camp_year,
        #     type(camp_year).__name__,
        #     group_type,
        #     type(group_type).__name__,
        # )
        logger.debug(
            "GET BY NATURAL KEY %s: (name: %s (%s), category: %s (%s))",
            "SubCategory",
            name,
            type(name).__name__,
            category,
            type(category).__name__,
        )

        if isinstance(category, list):
            return self.get(
                name=name,
                category__name=category[0],
                category__category_set__category_set__camp_year__year=category[1][0],
                category__category_set__group_type__group_type=category[1][1],
            )

        # if type(category).__name__ == "Category":
        # return self.get(name=name, category=category)

        # return self.get(
        #     name=name,
        #     category__category_set__category_set__camp_year__year=camp_year,
        #     category__category_set__group_type__group_type=group_type,
        # )
        return self.get(name=name, category=category)
