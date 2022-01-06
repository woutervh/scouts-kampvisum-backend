from rest_framework import serializers

from apps.visums.models import LinkedSubCategory
from apps.visums.serializers import SubCategorySerializer, LinkedCheckSerializer


class LinkedSubCategorySerializer(serializers.ModelSerializer):

    parent = SubCategorySerializer()
    checks = LinkedCheckSerializer(many=True)

    class Meta:
        model = LinkedSubCategory
        exclude = ["category"]
