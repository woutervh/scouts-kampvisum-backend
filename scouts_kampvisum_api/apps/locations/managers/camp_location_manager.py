import logging

from django.db import models
from django.db.models import Q
from django.conf import settings

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
            obj = self.safe_get_by_id(pk)
            if obj:
                return obj

        return None

    def exists(self, pk):
        if self.safe_get(pk=pk):
            return True

        return False
