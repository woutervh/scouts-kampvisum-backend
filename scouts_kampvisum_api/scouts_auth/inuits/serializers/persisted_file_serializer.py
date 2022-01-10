from django.core.files.storage import get_storage_class
from rest_framework import serializers

from scouts_auth.inuits.models import PersistedFile


class PersistedFileSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField()
    url = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = PersistedFile
        fields = "__all__"

    def get_url(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "name"):
            return get_storage_class()().url(obj.file.name)

    def get_name(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "name"):
            return obj.file.name

        return None

    def get_size(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "size"):
            return obj.file.size
