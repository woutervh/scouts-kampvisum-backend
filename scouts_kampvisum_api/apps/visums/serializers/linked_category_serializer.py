from rest_framework import serializers

from apps.visums.models import LinkedCategory
from apps.visums.serializers import CategorySerializer, LinkedSubCategorySerializer


class LinkedCategorySerializer(serializers.ModelSerializer):

    parent = CategorySerializer()
    sub_categories = LinkedSubCategorySerializer(many=True)

    class Meta:
        model = LinkedCategory
        exclude = ["category_set"]
