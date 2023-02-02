from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroupTypeQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScoutsGroupTypeManager(models.Manager):
    """
    Loads scouts group type instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return ScoutsGroupTypeQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        group_type = kwargs.get("group_type", None)
        is_default = kwargs.get("is_default", False)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if group_type:
            try:
                return self.get_queryset().get(group_type=group_type)
            except Exception:
                pass

        if is_default:
            try:
                return self.get_queryset().get(is_default=is_default)
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsGroupType instance with the provided params: (pk: ({}), group_type: ({}), is_default: ({})".format(
                    pk, group_type, is_default
                )
            )
        return None

    def get_by_natural_key(self, group_type):
        logger.trace(
            "GET BY NATURAL KEY %s: (group_type: %s (%s))",
            "ScoutsGroupType",
            group_type,
            type(group_type).__name__,
        )
        return self.get(group_type=group_type)
