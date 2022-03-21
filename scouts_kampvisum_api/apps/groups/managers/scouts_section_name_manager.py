from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionNameManager(models.Manager):
    """
    Loads ScoutsSectionName instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        name = kwargs.get("name", None)
        gender = kwargs.get("gender", None)
        age_group = kwargs.get("age_group", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if name and gender and age_group:
            try:
                return self.get_queryset().get(
                    name=name, gender=gender, age_group=age_group
                )
            except:
                pass

        if name and gender:
            results = list(self.get_queryset().all().filter(name=name, gender=gender))

            if len(results) == 1:
                return results[0]

            if len(results) > 1:
                raise ValidationError(
                    "ScoutsSectionName instances were found ({}) with name {} and gender {}, but age_group is required to return a single result".format(
                        len(results), name, gender
                    )
                )

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsSectionName instance with the provided params: (id: {}, (name: {}, gender: {}, age_group: {}))".format(
                    pk, name, gender, age_group
                )
            )
        return None

    def get_by_natural_key(self, name, gender, age_group):
        logger.trace(
            "GET BY NATURAL KEY %s: (name: %s (%s), gender: %s (%s), age_group: %s (%s))",
            "ScoutsSectionName",
            name,
            type(name).__name__,
            gender,
            type(gender).__name__,
            age_group,
            type(age_group).__name__,
        )
        return self.get(name=name, gender=gender, age_group=age_group)
