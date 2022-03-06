from django.db import models

from scouts_auth.inuits.files.validators import validate_uploaded_file
from scouts_auth.inuits.models import AuditedBaseModel

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PersistedFileQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PersistedFileManager(models.Manager):
    def get_queryset(self):
        return PersistedFileQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))

        if pk:
            try:
                logger.debug("Query PersistentFile with id %s", pk)
                return self.get_queryset().get(pk=pk)
            except:
                pass

        return None


class PersistedFile(AuditedBaseModel):
    objects = PersistedFileManager()

    file = models.FileField(
        validators=[validate_uploaded_file],
        null=True,
        blank=True,
    )
    content_type = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
