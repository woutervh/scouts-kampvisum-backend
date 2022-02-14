from rest_framework import serializers

from apps.locations.models import LinkedLocation
from apps.locations.serializers import CampLocationSerializer


class LinkedLocationSerializer(serializers.ModelSerializer):

    locations = CampLocationSerializer(many=True)

    class Meta:
        model = LinkedLocation
        fields = "__all__"
