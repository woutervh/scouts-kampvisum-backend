from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SubCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubCategoryManager(models.Manager):
    """
    Loads Category instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return SubCategoryQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        name = kwargs.get("name", None)
        category = kwargs.get("category", None)
        camp_types = kwargs.get("camp_types", [])
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if name:
            try:
                return self.get_queryset().get(name=name)
            except:
                pass

        if category and len(camp_types) > 0:
            try:
                return list(
                    self.get_queryset()
                    .filter(category=category, camp_types__in=camp_types)
                    .distinct()
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate SubCategory instance(s) with the provided params: (id: {}, name: {}, (category: {}, camp_types: {}))".format(
                    pk,
                    name,
                    category,
                    camp_types,
                    # ",".join(camp_type.camp_type for camp_type in camp_types),
                )
            )

        return None

    def get_by_natural_key(self, name, category):
        logger.trace(
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
                category__camp_year__year=category[1],
            )

        return self.get(name=name, category=category)
