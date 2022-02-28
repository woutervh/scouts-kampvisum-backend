import logging

from django.db import models
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


class ScoutsSectionNameManager(models.Manager):
    """
    Loads ScoutsSectionName instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, name, gender, age_group):
        logger.debug(
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

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsSectionName instance with the provided params: (id: {}, (name: {}, gender: {}, age_group: {}))".format(
                    pk, name, gender, age_group
                )
            )
        return None
