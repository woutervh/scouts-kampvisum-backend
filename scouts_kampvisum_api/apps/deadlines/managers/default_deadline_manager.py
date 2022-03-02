from django.db import models
from django.core.exceptions import ValidationError


import logging

logger = logging.getLogger(__name__)


class DefaultDeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DefaultDeadlineManager(models.Manager):
    def get_queryset(self):
        return DefaultDeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        name = kwargs.get("name", None)
        deadline_type = kwargs.get("deadline_type", None)
        camp_year = kwargs.get("camp_year", None)
        camp_types = kwargs.get("camp_types", [])
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if name and deadline_type:
            try:
                return self.get_queryset().get(name=name, deadline_type=deadline_type)
            except:
                pass

        if camp_year and len(camp_types) > 0:
            try:
                return self.get_queryset().filter(
                    camp_year=camp_year, camp_types__in=camp_types
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate DefaultDeadline instance(s) with the provided params: (id: {}, (name: {}, deadline_type: {}), (camp_year: {}, camp_types: {}))".format(
                    pk,
                    name,
                    deadline_type,
                    camp_year,
                    ",".join(camp_type.to_readable_str() for camp_type in camp_types),
                )
            )

        return None

    def get_by_natural_key(self, name, deadline_type, camp_year):
        logger.trace(
            "GET BY NATURAL KEY %s: (name: %s (%s), deadline_type: %s (%s), camp_year: %s (%s))",
            "DefaultDeadline",
            name,
            type(name).__name__,
            deadline_type,
            type(deadline_type).__name__,
            camp_year,
            type(camp_year).__name__,
        )

        return self.get(name=name, deadline_type=deadline_type, camp_year=camp_year)
