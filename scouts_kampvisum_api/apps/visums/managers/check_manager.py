import logging

from django.db import models


logger = logging.getLogger(__name__)


class CheckManager(models.Manager):
    """
    Loads Check instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name, sub_category):
        # logger.debug(
        #     "GET BY NATURAL KEY %s: (name: %s (%s), sub_category_name: %s (%s), category_name: %s (%s), camp_year: %s (%s), group_type: %s (%s))",
        #     "Check",
        #     name,
        #     type(name).__name__,
        #     sub_category_name,
        #     type(sub_category_name).__name__,
        #     category_name,
        #     type(category_name).__name__,
        #     camp_year,
        #     type(camp_year).__name__,
        #     group_type,
        #     type(group_type).__name__,
        # )
        logger.debug(
            "GET BY NATURAL KEY %s: (name: %s (%s), sub_category: %s (%s))",
            "Check",
            name,
            type(name).__name__,
            sub_category,
            type(sub_category).__name__,
        )

        # if type(category).__name__ == "Category":
        # return self.get(name=name, category=category)

        return self.get(name=name, sub_category=sub_category)
