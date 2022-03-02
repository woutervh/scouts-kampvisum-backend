from django.db import models

from scouts_auth.inuits.mixins import ArchivedOnModelMixin, ArchivedByModelMixin


class AuditArchiveModelMixin(ArchivedOnModelMixin, ArchivedByModelMixin, models.Model):

    is_archived = models.BooleanField(default=False)

    class Meta:
        abstract = True
