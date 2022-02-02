import logging

from django.conf import settings
from django.db import models


logger = logging.getLogger(__name__)


class ScoutsSectionQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        return self.filter(group_admin_id__in=user.get_group_names())


class ScoutsSectionManager(models.Manager):
    def get_queryset(self):
        return ScoutsSectionQuerySet(self.model, using=self._db)

    def get_by_natural_key(self, group_admin_id):
        logger.debug(
            "GET BY NATURAL KEY %s: (group_admin_id: %s (%s))",
            "ScoutsSection",
            group_admin_id,
            type(group_admin_id).__name__,
        )
        return self.get(group_admin_id=group_admin_id)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        return None
