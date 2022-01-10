from rest_framework import serializers

from apps.locations.models import CampLocation


class CampLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampLocation
        fields = "__all__"
