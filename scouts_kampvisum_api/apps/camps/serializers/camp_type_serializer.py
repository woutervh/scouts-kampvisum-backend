from rest_framework import serializers

from apps.camps.models import CampType


class CampTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampType
        fields = "__all__"
