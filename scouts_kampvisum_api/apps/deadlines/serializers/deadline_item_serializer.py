from rest_framework import serializers

from apps.deadlines.models import DeadlineItem
from apps.deadlines.serializers import (
    DefaultDeadlineItemSerializer,
    DeadlineFlagSerializer,
)

from apps.visums.models.enums import CheckState
from apps.visums.serializers import LinkedSubCategorySerializer, LinkedCheckSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineItemSerializer(serializers.ModelSerializer):

    parent = DefaultDeadlineItemSerializer()
    linked_sub_category = LinkedSubCategorySerializer(required=False)
    linked_check = LinkedCheckSerializer(required=False)
    flag = DeadlineFlagSerializer(required=False)

    class Meta:
        model = DeadlineItem
        fields = "__all__"

    def to_representation(self, obj: DeadlineItem) -> dict:
        logger.debug("DEADLINE ITEM: %s", obj)
        data = super().to_representation(obj)

        if obj.is_sub_category_deadline():
            data["linked_sub_category"]["category"] = {
                # "id": obj.linked_sub_category.category.id,
                # "name": obj.linked_sub_category.category.parent.name,
                # "label": obj.linked_sub_category.category.parent.label,
                "id": obj.linked_sub_category.id,
                "name": obj.linked_sub_category.parent.name,
                "label": obj.linked_sub_category.parent.label,
                "category": {
                    "id": obj.linked_sub_category.category.id,
                    "name": obj.linked_sub_category.category.parent.name,
                    "label": obj.linked_sub_category.category.parent.label,
                },
                "state": data.get("linked_sub_category").get(
                    "state", CheckState.UNCHECKED
                ),
            }
        elif obj.is_check_deadline():
            data["linked_check"]["category"] = {
                # "id": obj.linked_check.sub_category.category.id,
                # "name": obj.linked_check.sub_category.category.parent.name,
                # "label": obj.linked_check.sub_category.category.parent.label,
                "id": obj.linked_check.id,
                "name": obj.linked_check.parent.name,
                "label": obj.linked_check.parent.label,
                "category": {
                    "id": obj.linked_check.sub_category.category.id,
                    "name": obj.linked_check.sub_category.category.parent.name,
                    "label": obj.linked_check.sub_category.category.parent.label,
                },
                "state": data.get("linked_check").get("state", CheckState.UNCHECKED),
            }

        return data
