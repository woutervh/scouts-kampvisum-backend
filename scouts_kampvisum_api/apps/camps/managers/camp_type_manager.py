from django.db import models
from django.core.exceptions import ValidationError


import logging

logger = logging.getLogger(__name__)


class CampTypeQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def selectable(self, *args, **kwargs):
        return self.filter(is_default=False)


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
            except:
                pass

        if camp_type:
            try:
                return self.get_queryset().get(camp_type=camp_type)
            except:
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
        logger.trace(
            "GET BY NATURAL KEY %s: (camp_type: %s (%s))",
            "CampType",
            camp_type,
            type(camp_type).__name__,
        )

        if camp_type.strip() == "*":
            logger.trace("GET BY NATURAL KEY WITH expander (*)")

        return self.get(camp_type=camp_type)
