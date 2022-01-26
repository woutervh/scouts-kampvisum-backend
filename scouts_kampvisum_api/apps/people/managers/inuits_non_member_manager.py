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

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))

        if pk:
            logger.debug("pk: %s", pk)
            try:
                return self.get_queryset().get(pk=pk)
            except:
                logger.debug("hmmm")
                pass

        return None

    def exists(self, pk):
        if self.safe_get(pk=pk):
            return True

        return False
