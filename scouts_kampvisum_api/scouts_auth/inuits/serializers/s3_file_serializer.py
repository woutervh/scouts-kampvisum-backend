from django.core.files.storage import get_storage_class
from rest_framework import serializers

from scouts_auth.inuits.models import PersistedFile
from scouts_auth.inuits.files.validators import validate_uploaded_file

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class S3FileSerializer(serializers.Serializer):

    name = serializers.CharField(required=True)

    class Meta:
        abstract = True

class S3PresignedUrlFileSerializer(serializers.Serializer):

    presigned_url = serializers.CharField(required=True)

    class Meta:
        abstract = True
