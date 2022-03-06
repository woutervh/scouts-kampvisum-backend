from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCheckQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedCheckManager(models.Manager):
    """
    Loads LinkedCheck instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedCheckQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", True)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(
                    parent=parent, sub_category__category__category_set__visum=visum
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedCheck instance(s) with provided params (id: {}, (parent: {}, visum: {})".format(
                    pk, parent.to_simple_str(), visum
                )
            )
        return None
