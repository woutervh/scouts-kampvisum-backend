from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedSubCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def all(self, *args, **kwargs):
        return super().all(args, is_archived=False, **kwargs)


class LinkedSubCategoryManager(models.Manager):
    """
    Loads LinkedSubCategory instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedSubCategoryQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        category = kwargs.get("category", None)
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        is_archived = kwargs.get("is_archived", False)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if category and parent:
            try:
                return self.get_queryset().get(parent=parent, category=category)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(
                    parent__id=parent.id,
                    category__category_set__visum__id=visum.id,
                    is_archived=is_archived,
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedSubCategory instance(s) with provided params (id: {}, (category: {}, parent: {}), (parent: {}, visum: {})".format(
                    pk,
                    category.to_simple_str() if category else None,
                    parent.to_simple_str() if parent else None,
                    parent.to_simple_str() if parent else None,
                    visum,
                )
            )
        return None
