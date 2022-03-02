from rest_framework import serializers

from apps.camps.models import CampType


import logging

logger = logging.getLogger(__name__)


class CampTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampType
        fields = "__all__"
