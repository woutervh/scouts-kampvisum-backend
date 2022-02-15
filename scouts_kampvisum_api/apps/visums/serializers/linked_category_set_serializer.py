import logging

from rest_framework import serializers

from apps.visums.models import LinkedCategorySet
from apps.visums.models.enums import CheckState
from apps.visums.serializers import CategorySetSerializer, LinkedCategorySerializer


logger = logging.getLogger(__name__)


class LinkedCategorySetSerializer(serializers.ModelSerializer):

    parent = CategorySetSerializer()
    categories = LinkedCategorySerializer(many=True)

    class Meta:
        model = LinkedCategorySet
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        return {}

    def to_representation(self, obj: LinkedCategorySet) -> dict:
        # logger.debug("LINKED CATEGORY SET SERIALIZER TO_REPRESENTATION: %s", obj)

        data = super().to_representation(obj)

        # logger.debug("LINKED CATEGORY SET SERIALIZER TO_REPRESENTATION: %s", data)

        data["state"] = CheckState.CHECKED
        for category in data.get("categories", []):
            if CheckState.is_unchecked(category.get("state", CheckState.UNCHECKED)):
                data["state"] = CheckState.UNCHECKED
                break

        data["readable_name"] = obj.readable_name

        return data
