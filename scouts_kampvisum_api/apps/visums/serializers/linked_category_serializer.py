from rest_framework import serializers

from apps.visums.models import LinkedCategory
from apps.visums.serializers import LinkedCategorySetSerializer, CategorySerializer


class LinkedCategorySerializer(serializers.ModelSerializer):

    parent = CategorySerializer()
    category_set = LinkedCategorySetSerializer()

    class Meta:
        model = LinkedCategory
        fields = "__all__"
