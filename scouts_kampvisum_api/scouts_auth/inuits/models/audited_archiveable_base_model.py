from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.mixins import (
    AuditCreateModelMixin,
    AuditUpdateModelMixin,
    AuditArchiveModelMixin,
)


class AuditedArchiveableBaseModel(
    AbstractBaseModel,
    AuditCreateModelMixin,
    AuditUpdateModelMixin,
    AuditArchiveModelMixin,
):
    """Abstract base models that can be archived and logs create and update events for time and user. (field names: created_by, created_on, updated_by, updated_on, is_archived, archived_by, archived_on)"""

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
