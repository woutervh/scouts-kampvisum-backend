from rest_framework import serializers

from apps.camps.serializers import CampYearSerializer
from apps.visums.models import CampYearCategorySet


class CampYearCategorySetSerializer(serializers.Serializer):

    camp_year = CampYearSerializer()

    class Meta:
        model = CampYearCategorySet
        fields = "__all__"
