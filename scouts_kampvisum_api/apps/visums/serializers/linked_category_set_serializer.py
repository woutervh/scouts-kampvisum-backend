from rest_framework import serializers

from apps.visums.models import LinkedCategorySet
from apps.visums.serializers import CategorySetSerializer


class LinkedCategorySetSerializer(serializers.ModelSerializer):

    parent = CategorySetSerializer

    class Meta:
        model = LinkedCategorySet
        fields = "__all__"
