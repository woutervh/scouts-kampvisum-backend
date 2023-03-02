
from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField


class S3File(AuditedBaseModel):

    original_name = RequiredCharField()
    path = RequiredCharField()
