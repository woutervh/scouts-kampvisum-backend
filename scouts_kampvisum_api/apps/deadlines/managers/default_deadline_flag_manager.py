from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultDeadlineFlagQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DefaultDeadlineFlagManager(models.Manager):
    def get_queryset(self):
        return DefaultDeadlineFlagQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        # deadline_item = kwargs.get("deadline_item", None)
        name = kwargs.get("name", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        # if deadline_item and name:
        #     try:
        #         return self.get_queryset().get(deadline_item=deadline_item, name=name)
        #     except:
        #         pass
        if name:
            try:
                return self.get_queryset().get(name=name)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate DefaultDeadlineFlag instance(s) with the provided params: (id: {}, name: {})".format(
                    pk,
                    name,
                )
            )
        return None

    # def get_by_natural_key(self, deadline_item, name):
    #     logger.trace(
    #         "GET BY NATURAL KEY %s: (deadline_item: %s (%s),  name: %s (%s))",
    #         "DefaultDeadlineFlag",
    #         deadline_item,
    #         type(deadline_item).__name__,
    #         name,
    #         type(name).__name__,
    #     )

    #     return self.get(deadline_item=deadline_item, name=name)
    def get_by_natural_key(self, name):
        logger.trace(
            "GET BY NATURAL KEY %s: (name: %s (%s))",
            "DefaultDeadlineFlag",
            name,
            type(name).__name__,
        )

        return self.get(name=name)
