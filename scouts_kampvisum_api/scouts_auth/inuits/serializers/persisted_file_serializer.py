from django.core.files.storage import get_storage_class
from rest_framework import serializers

from scouts_auth.inuits.models import PersistedFile
from scouts_auth.inuits.files.validators import validate_uploaded_file

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PersistedFileSerializer(serializers.ModelSerializer):

    # id = serializers.UUIDField(required=False, null=True)
    file = serializers.FileField(required=False)
    content_type = serializers.CharField(required=False)
    url = serializers.SerializerMethodField(required=False)
    name = serializers.SerializerMethodField(required=False)
    size = serializers.SerializerMethodField(required=False)

    class Meta:
        model = PersistedFile
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("PERSISTED FILE SERIALIZER TO INTERNAL VALUE: %s", data)
        data["uuid_location"] = data.get("uuid_location")

        # If an id is present, assume it is a simple instance input
        file = PersistedFile.objects.safe_get(pk=data.get("id", None))
        if file:
            return file

        original_name = data.get("original_name", None)
        if not original_name:
            data["original_name"] = data.get("file").name

        data = super().to_internal_value(data)

        logger.debug("PERSISTED FILE SERIALIZER TO INTERNAL VALUE: %s", data)

        return data

    def to_representation(self, value):
        return {
            "id": value.id,
            "name": self.get_name(value),
            "original_name": value.original_name,
            "content_type": value.content_type,
            "created_by": value.created_by,
            "created_on": value.created_on,
            "updated_by": value.updated_by,
            "updated_on": value.updated_on,
        }

    def get_url(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "name"):
            return get_storage_class()().url(obj.file.name)

    def get_name(self, obj: PersistedFile):
        # if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "name"):
        #     return obj.file.name

        # return None
        return obj.original_name

    def get_size(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "size"):
            return obj.file.size


class PersistedFileDetailedSerializer(serializers.ModelSerializer):

    # id = serializers.UUIDField(required=False, null=True)
    file = serializers.FileField(required=False)
    content_type = serializers.CharField(required=False)
    url = serializers.SerializerMethodField(required=False)
    name = serializers.SerializerMethodField(required=False)
    size = serializers.SerializerMethodField(required=False)

    class Meta:
        model = PersistedFile
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("PERSISTED FILE SERIALIZER TO INTERNAL VALUE: %s", data)

        # If an id is present, assume it is a simple instance input
        file = PersistedFile.objects.safe_get(pk=data.get("id", None))
        if file:
            return file

        original_name = data.get("original_name", None)
        if not original_name:
            data["original_name"] = data.get("file").name

        data = super().to_internal_value(data)

        logger.debug("PERSISTED FILE SERIALIZER TO INTERNAL VALUE: %s", data)

        return data

    def get_url(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "name"):
            return get_storage_class()().url(obj.file.name)

    def get_name(self, obj: PersistedFile):
        # if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "name"):
        #     return obj.file.name

        # return None
        return obj.original_name

    def get_size(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "size"):
            return obj.file.size
