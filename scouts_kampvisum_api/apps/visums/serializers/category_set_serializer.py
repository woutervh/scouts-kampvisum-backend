from rest_framework import serializers

from apps.visums.models import CategorySet
from apps.visums.serializers import (
    CampYearCategorySetSerializer,
    CampTypeSerializer,
    CategorySetPrioritySerializer,
    CategorySerializer,
)


class CategorySetSerializer(serializers.ModelSerializer):

    camp_year_category_set = CampYearCategorySetSerializer()
    camp_type = CampTypeSerializer()
    priority = CategorySetPrioritySerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = CategorySet
        fields = "__all__"
