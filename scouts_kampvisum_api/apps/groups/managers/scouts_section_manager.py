from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import ScoutsGroup


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        return self.filter(group_admin_id__in=user.get_group_names())


class ScoutsSectionManager(models.Manager):
    def get_queryset(self):
        return ScoutsSectionQuerySet(self.model, using=self._db)

    def get_by_natural_key(self, group, name):
        logger.trace(
            "GET BY NATURAL KEY %s: (group: %s (%s), name: %s (%s))",
            "ScoutsSection",
            group,
            type(group).__name__,
            name,
            type(name).__name__,
        )

        if isinstance(group, ScoutsGroup):
            return self.get(group=group, name=name)

        return self.get(group__group_admin_id=group, name=name)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        group = kwargs.get("group", None)
        group_group_admin_id = kwargs.get("group_group_admin_id", None)
        name = kwargs.get("name", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if name:
            if group:
                try:
                    return self.get_queryset().get(group=group, name=name)
                except:
                    pass

            if group_group_admin_id:
                try:
                    return self.get_queryset().get(
                        group__group_admin_id=group_group_admin_id, name=name
                    )
                except:
                    pass

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsSection instance with the provided params: (pk: ({}), (group: ({}), name: ({})), (group_group_admin_id: ({}), name ({})))".format(
                    pk, group, name, group_group_admin_id, name
                )
            )
        return None
