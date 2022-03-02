from django.db import models
from django.core.exceptions import ValidationError


import logging

logger = logging.getLogger(__name__)


class LinkedSubCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedSubCategoryManager(models.Manager):
    """
    Loads LinkedSubCategory instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedSubCategoryQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(
                    parent__id=parent.id, category__category_set__visum__id=visum.id
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedSubCategory instance(s) with provided params (id: {}, (parent: {}, visum: {})".format(
                    pk, parent.to_simple_str(), visum
                )
            )
        return None
