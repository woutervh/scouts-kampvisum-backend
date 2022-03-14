from django.db import models

from scouts_auth.inuits.mixins import UpdatedOnModelMixin, UpdatedByModelMixin


class AuditUpdateModelMixin(UpdatedOnModelMixin, UpdatedByModelMixin, models.Model):
    """Specifies by who and when the object was updated (field names: updated_by, updated_on)"""

    class Meta:
        abstract = True
