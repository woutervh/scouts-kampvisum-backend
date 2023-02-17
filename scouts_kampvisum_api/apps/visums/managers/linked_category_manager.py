from django.db import models, connections
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def count_unchecked_checks(self, pk):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select count(1) from visums_linkedsubcategory vl where vl.category_id = '{pk}' and vl.check_state = 'UNCHECKED'"
            )
            return cursor.fetchone()[0]

        return 1

    def get_for_visum(self, visum_id):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select lc.id as id, lc.check_state as check_state, c.name as name, c.label as label, c.description as description, c.explanation as explanation, c.index as index from visums_linkedcategory lc left join visums_category c on c.id = lc.parent_id left join visums_linkedcategoryset lcs on lcs.id = lc.category_set_id where lcs.visum_id = '{visum_id}' order by c.index"
            )
            return cursor.fetchall()
        return None


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
            except Exception:
                pass

        if category_set and parent:
            try:
                return self.get_queryset().get(
                    category_set=category_set,
                    parent=parent,
                    is_archived=is_archived,
                )
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedCategory instance(s) with provided params (id: {}, (category_set: {}, parent: {}))".format(
                    pk, category_set if category_set else None, parent.to_simple_str() if parent else None
                )
            )
        return None

    def has_unchecked_checks(self, pk):
        return True if self.get_queryset().count_unchecked_checks(pk=pk) == 0 else False

    def get_for_visum(self, visum_id):
        results = self.get_queryset().get_for_visum(visum_id=visum_id)

        categories = []
        for result in results:
            categories.append({
                "id": result[0],
                "state": result[1],
                "parent": {
                    "name": result[2],
                    "label": result[3],
                    "description": result[4],
                    "explanation": result[5],
                    "index": result[6],
                }
            })
        return categories
