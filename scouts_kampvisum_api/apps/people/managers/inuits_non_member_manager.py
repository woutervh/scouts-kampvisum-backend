import logging

from django.db import models
from django.conf import settings

logger = logging.getLogger(__name__)


class InuitsNonMemberQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def allowed(self, user: settings.AUTH_USER_MODEL):
        groups = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_group_admin_id__in=groups)


class InuitsNonMemberManager(models.Manager):
    def get_queryset(self):
        # Return InuitsNonMember instances that can show up in searches
        return InuitsNonMemberQuerySet(self.model, using=self._db)
