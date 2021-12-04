from rest_framework import serializers

from apps.visums.models import CategorySet
from apps.visums.serializers import (
    CategorySetPrioritySerializer,
    CategorySerializer,
    CategoryAPISerializer,
)
from apps.groups.serializers import ScoutsGroupTypeSerializer
from apps.camps.serializers import CampYearSerializer


class CategorySetSerializer(serializers.ModelSerializer):

    priority = CategorySetPrioritySerializer()
    type = ScoutsGroupTypeSerializer()
    categories = CategorySerializer(many=True)
    camp_year = CampYearSerializer()
    is_default = serializers.BooleanField(default=False)

    class Meta:
        model = CategorySet
        fields = "__all__"


class CategorySetAPISerializer(serializers.ModelSerializer):

    categories = CategoryAPISerializer(many=True)

    class Meta:
        model = CategorySet
        fields = ["categories"]
