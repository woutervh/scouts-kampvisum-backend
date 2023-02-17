from django.db import models, connections
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampTypeQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def selectable(self, *args, **kwargs):
        return self.filter(is_default=False)

    def get_for_visum(self, visum_id):
        with connections["default"].cursor() as cursor:
            cursor.execute(
                f"select ct.id as id, ct.camp_type as camp_type, ct.is_base as is_base, ct.is_default as is_default from camps_camptype ct left join visums_campvisum_camp_types vct on ct.id = vct.camptype_id where vct.campvisum_id='{visum_id}'"
            )
            return cursor.fetchall()
        return None


class CampTypeManager(models.Manager):
    """
    Loads CampType instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CampTypeQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        camp_type = kwargs.get("camp_type", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if camp_type:
            try:
                return self.get_queryset().get(camp_type=camp_type)
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate CampType instance with provided params (id: {}, camp_type: {})".format(
                    pk, camp_type
                )
            )
        return None

    def get_default(self):
        return self.get_queryset().get(is_default=True)

    def get_by_natural_key(self, camp_type):
        # logger.trace(
        #     "GET BY NATURAL KEY %s: (camp_type: %s (%s))",
        #     "CampType",
        #     camp_type,
        #     type(camp_type).__name__,
        # )

        if camp_type.strip() == "*":
            logger.trace("GET BY NATURAL KEY WITH expander (*)")

        return self.get(camp_type=camp_type)

    def get_for_visum(self, visum_id):
        results = self.get_queryset().get_for_visum(visum_id=visum_id)

        camp_types = []
        for result in results:
            camp_types.append({
                "id": result[0],
                "camp_type": result[1],
                "is_base": result[2],
                "is_default": result[3],
            })
        return camp_types
