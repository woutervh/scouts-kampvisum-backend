import logging

from django.db import models


logger = logging.getLogger(__name__)


class DefaultDeadlineSetQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DefaultDeadlineSetManager(models.Manager):
    def get_queryset(self):
        return DefaultDeadlineSetQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        camp_year = kwargs.get("camp_year", None)
        camp_type = kwargs.get("camp_type", None)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if camp_year and camp_type:
            try:
                return self.get_queryset().get(camp_year=camp_year, camp_type=camp_type)
            except:
                pass

        return None

    def get_by_natural_key(self, camp_year, camp_type):
        logger.debug(
            "GET BY NATURAL KEY %s: (camp_year: %s (%s), camp_type: %s (%s))",
            "DefaultDeadlineSet",
            camp_year,
            type(camp_year).__name__,
            camp_type,
            type(camp_type).__name__,
        )

        return self.get(camp_year=camp_year, camp_type=camp_type)
