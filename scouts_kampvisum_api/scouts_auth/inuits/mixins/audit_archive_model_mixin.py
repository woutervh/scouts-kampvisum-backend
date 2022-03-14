from django.db import models

from scouts_auth.inuits.mixins import ArchivedOnModelMixin, ArchivedByModelMixin


class AuditArchiveModelMixin(ArchivedOnModelMixin, ArchivedByModelMixin, models.Model):
    """Specifies if the object is archived, by who and when (field names: is_archived, archived_by, archived_on)"""

    is_archived = models.BooleanField(default=False)

    class Meta:
        abstract = True
