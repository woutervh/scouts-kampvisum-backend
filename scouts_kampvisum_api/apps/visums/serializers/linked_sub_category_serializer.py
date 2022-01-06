from rest_framework import serializers

from apps.visums.models import LinkedSubCategory
from apps.visums.serializers import LinkedCategorySerializer, SubCategorySerializer


class LinkedSubCategorySerializer(serializers.ModelSerializer):

    parent = SubCategorySerializer()
    category = LinkedCategorySerializer()

    class Meta:
        model = LinkedSubCategory
        fields = "__all__"
