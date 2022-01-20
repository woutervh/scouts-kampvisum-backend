from django.core.files.storage import get_storage_class
from rest_framework import serializers

from scouts_auth.inuits.models import PersistedFile


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
