from django.db import models
from django.conf import settings


import logging

logger = logging.getLogger(__name__)


class CampLocationQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def allowed(self, user: settings.AUTH_USER_MODEL):
        groups = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_group_admin_id__in=groups)


class CampLocationManager(models.Manager):
    def get_queryset(self):
        return CampLocationQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))

        if pk:
            try:
                logger.debug("here")
                return self.get_queryset().get(pk=pk)
            except:
                pass
        logger.debug("hmmmm")
        return None

    def exists(self, pk):
        if self.safe_get(pk=pk):
            return True

        return False
