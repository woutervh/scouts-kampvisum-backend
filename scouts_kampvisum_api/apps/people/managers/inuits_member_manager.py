import logging

from django.db import models
from django.conf import settings


logger = logging.getLogger(__name__)


class InuitsMemberQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def allowed(self, user: settings.AUTH_USER_MODEL):
        groups = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_group_admin_id__in=groups)


class InuitsMemberManager(models.Manager):
    def get_queryset(self):
        # Return InuitsNonMember instances that can show up in searches
        return InuitsMemberQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        group_admin_id = kwargs.get("group_admin_id", None)

        if group_admin_id and not pk:
            return self.safe_get_by_group_admin_id(group_admin_id)

        if pk:
            obj = self.safe_get_by_id(pk)

            if obj:
                return obj

        if group_admin_id:
            return self.safe_get_by_group_admin_id(group_admin_id)

        return None

    def safe_get_by_id(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except:
            return None

    def safe_get_by_group_admin_id(self, group_admin_id):
        try:
            return self.get_queryset().get(group_admin_id=str(group_admin_id))
        except:
            return None
