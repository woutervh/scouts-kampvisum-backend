from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineManager(models.Manager):
    def get_queryset(self):
        return DeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        name = kwargs.get("name", None)
        camp_year = kwargs.get("camp_year", None)
        camp_types = kwargs.get("camp_types", [])
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if name and camp_year:
            try:
                return self.get_queryset().get(name=name, camp_year=camp_year)
            except Exception:
                pass

        if camp_year and len(camp_types) > 0:
            try:
                return self.get_queryset().filter(
                    camp_year=camp_year, camp_types__in=camp_types
                )
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate Deadline instance(s) with the provided params: (id: {}, (name: {}, (camp_year: {}, camp_types: {}))".format(
                    pk,
                    name,
                    camp_year,
                    ",".join(camp_type.to_readable_str()
                             for camp_type in camp_types),
                )
            )

        return None

    def get_by_natural_key(self, name, camp_year):
        logger.trace(
            "GET BY NATURAL KEY %s: (name: %s (%s), camp_year: %s (%s))",
            "Deadline",
            name,
            type(name).__name__,
            camp_year,
            type(camp_year).__name__,
        )

        return self.get(name=name, camp_year=camp_year)
