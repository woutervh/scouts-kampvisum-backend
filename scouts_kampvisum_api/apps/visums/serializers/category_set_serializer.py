from rest_framework import serializers

from apps.visums.models import CategorySet
from apps.visums.serializers import (
    CampYearCategorySetSerializer,
    CategorySetPrioritySerializer,
    CategoryAPISerializer,
)
from apps.groups.serializers import ScoutsGroupTypeSerializer


class CategorySetSerializer(serializers.ModelSerializer):

    category_set = CampYearCategorySetSerializer()
    priority = CategorySetPrioritySerializer()
    # categories = CategorySerializer(many=True)
    # camp_year = CampYearSerializer()
    # is_default = serializers.BooleanField(default=False)

    class Meta:
        model = CategorySet
        fields = "__all__"


class CategorySetAPISerializer(serializers.ModelSerializer):

    categories = CategoryAPISerializer(many=True)

    class Meta:
        model = CategorySet
        fields = ["categories"]
