import logging

from django.db import models

from scouts_auth.inuits.files.validators import validate_file_extension
from scouts_auth.inuits.models import AuditedBaseModel


logger = logging.getLogger(__name__)


class PersistedFile(AuditedBaseModel):
    file = models.FileField(
        validators=[validate_file_extension],
        null=True,
        blank=True,
    )
    content_type = models.CharField(max_length=100)
