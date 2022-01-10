from rest_framework import serializers

from scouts_auth.inuits.models import PersistedFile


class PersistedFileSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField()
    name = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = PersistedFile

    def get_name(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "name"):
            return obj.file.name

        return None

    def get_size(self, obj: PersistedFile):
        if obj and hasattr(obj, "file") and obj.file and hasattr(obj.file, "size"):
            return obj.file.size
