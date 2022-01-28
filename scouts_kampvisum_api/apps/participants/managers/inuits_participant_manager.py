import logging

from django.db import models
from django.db.models import Q
from django.conf import settings

logger = logging.getLogger(__name__)


class InuitsParticipantQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def allowed(self, user: settings.AUTH_USER_MODEL):
        groups = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_group_admin_id__in=groups)

    def members(self):
        return self.filter(Q(is_member=True) & Q(group_admin_id__isnull=False))

    def non_members(self):
        return self.filter(Q(is_member=False) & Q(group_admin_id__isnull=True))


class InuitsParticipantManager(models.Manager):
    def get_queryset(self):
        return InuitsParticipantQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        group_admin_id = kwargs.get("group_admin_id", None)
        email = kwargs.get("email", None)

        if group_admin_id and not pk:
            return self.safe_get_by_group_admin_id(group_admin_id)

        if pk:
            obj = self.safe_get_by_id(pk)
            if obj:
                return obj

        if group_admin_id:
            obj = self.safe_get_by_group_admin_id(group_admin_id)
            if obj:
                return obj
        
        if email:
            obj = self.safe_get_by_email(email)
            if obj:
                return obj

        return None

    def safe_get_by_id(self, pk):
        try:
            logger.debug("Query InuitsParticipant with id %s", pk)
            return self.get_queryset().get(pk=pk)
        except:
            return None

    def safe_get_by_group_admin_id(self, group_admin_id):
        try:
            logger.debug("Query InuitsParticipant with group admin id %s", group_admin_id)
            return self.get_queryset().get(group_admin_id=str(group_admin_id))
        except:
            return None
    
    def safe_get_by_email(self, email):
        try:
            logger.debug("Query InuitsParticipant with email %s", email)
            return self.get_queryset().get(email=email)
        except:
            return None

    def exists(self, pk):
        if self.safe_get(pk=pk):
            return True

        return False
