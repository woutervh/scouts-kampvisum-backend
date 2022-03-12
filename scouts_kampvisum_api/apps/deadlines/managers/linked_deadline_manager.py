from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedDeadlineManager(models.Manager):
    def get_queryset(self):
        return LinkedDeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        parent_name = kwargs.get("parent_name", None)
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(parent=parent, visum=visum)
            except:
                pass
        
        if parent_name and visum:
            try:
                return self.get_queryset().get(parent__name=parent_name, visum=visum)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedDeadline instance with provided params (pk: {}, (parent: {}, visum: {}), (parent_name: {}, visum: {}))".format(
                    pk, parent, visum, parent_name, visum
                )
            )
        return None
