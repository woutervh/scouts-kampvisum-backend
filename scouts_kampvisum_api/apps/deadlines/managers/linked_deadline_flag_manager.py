from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineFlagQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedDeadlineFlagManager(models.Manager):
    def get_queryset(self):
        return LinkedDeadlineFlagQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        linked_deadline = kwargs.get("linked_deadline", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if parent and linked_deadline:
            try:
                return self.get_queryset().get(
                    parent=parent, linked_deadline=linked_deadline
                )
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedDeadlineFlag instance with provided params (id: {}, (parent: {}, linked_deadline: {})".format(
                    pk, parent, linked_deadline
                )
            )
        return None
