from rest_framework import serializers

from ..models import CategorySet
from ..serializers import (
    CategorySetPrioritySerializer,
    CategorySerializer,
    CategoryAPISerializer,
)
from apps.groups.api.serializers import GroupTypeSerializer
from apps.camps.serializers import CampYearSerializer
from inuits.mixins import FlattenMixin


class CategorySetSerializer(serializers.ModelSerializer):

    priority = CategorySetPrioritySerializer()
    type = GroupTypeSerializer()
    categories = CategorySerializer(many=True)
    camp_year = CampYearSerializer()
    is_default = serializers.BooleanField(default=False)

    class Meta:
        model = CategorySet
        fields = "__all__"


class CampVisumCategorySetAPISerializer(serializers.ModelSerializer):

    categories = CategoryAPISerializer(many=True)

    class Meta:
        model = CategorySet
        fields = ["categories"]
