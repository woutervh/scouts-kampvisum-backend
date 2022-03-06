from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineDateQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineDateManager(models.Manager):
    def get_queryset(self):
        return DeadlineDateQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        default_deadline = kwargs.get("default_deadline", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if default_deadline:
            try:
                return self.get_queryset().get(default_deadline=default_deadline)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate DefaultDeadline instance(s) with the provided params: (id: {}, default_deadline: {})".format(
                    pk,
                    default_deadline,
                )
            )
        return None

    def get_by_natural_key(self, default_deadline):
        logger.trace(
            "GET BY NATURAL KEY %s: (default_deadline: %s (%s))",
            "DeadlineDate",
            default_deadline,
            type(default_deadline).__name__,
        )

        return self.get(default_deadline=default_deadline)
