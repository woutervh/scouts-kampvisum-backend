from django.db import models

from scouts_auth.inuits.mixins import CreatedOnModelMixin, CreatedByModelMixin


class AuditCreateModelMixin(CreatedOnModelMixin, CreatedByModelMixin, models.Model):
    """Specifies by who and when the object was created (field names: created_by, created_on)"""

    class Meta:
        abstract = True
