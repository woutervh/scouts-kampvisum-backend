from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedCategoryManager(models.Manager):
    """
    Loads LinkedSubCategory instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedCategoryQuerySet(self.model, using=self._db).prefetch_related('parent', 'sub_categories')

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        category_set = kwargs.get("category_set", None)
        parent = kwargs.get("parent", None)
        is_archived = kwargs.get("is_archived", False)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if category_set and parent:
            try:
                return self.get_queryset().get(
                    category_set=category_set,
                    parent=parent,
                    is_archived=is_archived,
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedCategory instance(s) with provided params (id: {}, (category_set: {}, parent: {}))".format(
                    pk, parent.to_simple_str() if parent else None
                )
            )
        return None
