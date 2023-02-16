from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineFlagQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineFlagManager(models.Manager):
    def get_queryset(self):
        return DeadlineFlagQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        name = kwargs.get("name", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if name:
            try:
                return self.get_queryset().get(name=name)
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate DeadlineFlag instance(s) with the provided params: (id: {}, name: {})".format(
                    pk,
                    name,
                )
            )
        return None

    def get_by_natural_key(self, name):
        logger.trace(
            "GET BY NATURAL KEY %s: (name: %s (%s))",
            "DeadlineFlag",
            name,
            type(name).__name__,
        )

        return self.get(name=name)
