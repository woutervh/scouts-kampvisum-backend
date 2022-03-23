from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultScoutsSectionNameQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DefaultScoutsSectionNameManager(models.Manager):
    """
    Loads DefaultScoutsSectionName instances by their group type and name, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return DefaultScoutsSectionNameQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        group_type = kwargs.get("group_type", None)
        name = kwargs.get("name", None)
        gender = kwargs.get("gender", None)
        age_group = kwargs.get("age_group", None)
        return_list = kwargs.get("return_list", False)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if group_type:
            if return_list and gender:
                try:
                    return (
                        self.get_queryset()
                        .filter(group_type=group_type, name__gender=gender)
                        .distinct()
                    )
                except:
                    pass

            if name and gender and age_group:
                try:
                    return self.get_queryset().get(
                        group_type=group_type,
                        name=name,
                        gender=gender,
                        age_group=age_group,
                    )
                except:
                    pass

            if gender and age_group:
                try:
                    return self.get_queryset().get(
                        group_type=group_type,
                        gender=gender,
                        age_group=age_group,
                    )
                except:
                    pass

        if raise_error:
            raise ValidationError(
                "Unable to locate DefaultScoutsSectionName instance with the provided params: (pk: ({}), (group_type: ({}), name: ({}), gender: ({}), age_group: ({}))".format(
                    pk, group_type, name, gender, age_group
                )
            )
        return None

    def safe_get_list(self, *args, **kwargs):
        return self.safe_get(*args, return_list=True, **kwargs)

    def get_by_natural_key(self, group_type, name, gender, age_group):
        logger.trace(
            "GET BY NATURAL KEY %s: (group_type: %s (%s), name: %s (%s), gender: %s (%s), age_group: %s (%s))",
            "DefaultScoutsSectionName",
            group_type,
            type(group_type).__name__,
            name,
            type(name).__name__,
            gender,
            type(gender).__name__,
            age_group,
            type(age_group).__name__,
        )
        return self.get(
            group_type=group_type, name=name, gender=gender, age_group=age_group
        )
