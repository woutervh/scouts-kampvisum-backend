from rest_framework import serializers

from apps.visums.models import LinkedCategorySet
from apps.visums.serializers import CategorySetSerializer, LinkedCategorySerializer


class LinkedCategorySetSerializer(serializers.ModelSerializer):

    parent = CategorySetSerializer()
    categories = LinkedCategorySerializer(many=True)

    class Meta:
        model = LinkedCategorySet
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        return {}
