from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


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
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if group_admin_id:
            try:
                return self.get_queryset().get(group_admin_id=str(group_admin_id))
            except:
                pass

        if email:
            try:
                return self.get_queryset().get(email=email)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate InuitsParticipant instance with the provide params: (pk: {}, group_admin_id: {}, email: {}".format(
                    pk, group_admin_id, email
                )
            )

        return None

    def exists(self, pk):
        if self.safe_get(pk=pk):
            return True

        return False
