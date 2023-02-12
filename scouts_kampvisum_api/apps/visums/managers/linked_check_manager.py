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
        return LinkedCheckQuerySet(self.model, using=self._db).prefetch_related('parent')

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        sub_category = kwargs.get("sub_category", None)
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        linked_to = kwargs.get("linked_to", None)
        is_archived = kwargs.get("is_archived", False)
        raise_error = kwargs.get("raise_error", False)

        filters = {}
        if pk:
            filters = {"pk": pk}
        elif (sub_category and parent):
            filters = {"sub_category": sub_category, "parent": parent}
        elif (parent and visum):
            filters = {"parent": parent, "sub_category__category__category_set__visum": visum,
                       "is_archived": is_archived}
        elif (visum and linked_to):
            filters = {"sub_category__category__category_set__visum": visum,
                       "parent__name": linked_to}

        try:
            return self.get_queryset().get(**filters)
        except Exception:
            pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedCheck instance(s) with provided params (id: {}, (sub_category: {}, parent: {}), (parent: {}, visum: {}), (linked_to: {}, visum: {})".format(
                    pk,
                    sub_category.to_simple_str() if sub_category else None,
                    parent.to_simple_str() if parent else None,
                    parent.to_simple_str() if parent else None,
                    visum.to_simple_str() if visum else None,
                    linked_to if linked_to else None,
                    visum.to_simple_str() if visum else None,
                )
            )
        return None
