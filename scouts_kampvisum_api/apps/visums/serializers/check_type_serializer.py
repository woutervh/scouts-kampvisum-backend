from rest_framework import serializers

from apps.visums.models import CheckType


class CheckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckType
        fields = "__all__"
