from typing import List

from django.db import models, connections
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CheckManager(models.Manager):
    """
    Loads Check instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CheckQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        sub_category = kwargs.get("sub_category", None)
        camp_types = kwargs.get("camp_types", [])
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if sub_category and len(camp_types) > 0:
            try:
                return list(
                    self.get_queryset().filter(
                        sub_category=sub_category, camp_types__in=camp_types
                    )
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate Check instance(s) with the provided params: (id: {}, (sub_category: {}, camp_types: {}))".format(
                    pk, sub_category, camp_types
                )
            )

        return None

    def get_by_natural_key(self, name, sub_category):
        logger.trace(
            "GET BY NATURAL KEY %s: (name: %s (%s), sub_category: %s (%s))",
            "Check",
            name,
            type(name).__name__,
            sub_category,
            type(sub_category).__name__,
        )

        if isinstance(sub_category, list):
            return self.get(
                name=name,
                sub_category__name=sub_category[0],
                sub_category__category__name=sub_category[1][0],
                sub_category__category__camp_year__year=sub_category[1][1],
            )

        return self.get(name=name, sub_category=sub_category)
