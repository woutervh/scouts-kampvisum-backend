from django.core.files.storage import get_storage_class
from rest_framework import serializers

from scouts_auth.inuits.models import PersistedFile
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.files.validators import validate_uploaded_file

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class S3FileSerializer(serializers.Serializer):

    name = RequiredCharField(max_length=256)

    class Meta:
        abstract = True

    def to_internal_value(self, data: dict):
        return data


class S3PresignedUrlFileSerializer(serializers.Serializer):

    presigned_url = RequiredCharField()

    class Meta:
        abstract = True


class S3PresignedUrlPostFileSerializer(serializers.Serializer):

    original_name = RequiredCharField()
    directory_path = RequiredCharField()
    url = RequiredCharField()
    fields = serializers.JSONField()

    class Meta:
        abstract = True

    def to_representation(self, data: dict) -> dict:
        return data
