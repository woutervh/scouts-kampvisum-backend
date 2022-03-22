from rest_framework import serializers

from apps.deadlines.models import LinkedDeadlineItem
from apps.deadlines.serializers import (
    DeadlineItemSerializer,
    LinkedDeadlineFlagSerializer,
)

from apps.visums.models.enums import CheckState
from apps.visums.serializers import LinkedSubCategorySerializer, LinkedCheckSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineItemSerializer(serializers.ModelSerializer):

    parent = DeadlineItemSerializer()
    linked_sub_category = LinkedSubCategorySerializer(required=False)
    linked_check = LinkedCheckSerializer(required=False)
    flag = LinkedDeadlineFlagSerializer(required=False)

    class Meta:
        model = LinkedDeadlineItem
        fields = "__all__"

    def to_representation(self, obj: LinkedDeadlineItem) -> dict:
        # logger.debug("LINKED DEADLINE ITEM: %s", obj)
        data = super().to_representation(obj)

        state = CheckState.UNCHECKED
        if obj.is_sub_category_deadline():
            state = data.get("linked_sub_category").get("state", CheckState.UNCHECKED)
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
                "state": state,
            }
        elif obj.is_check_deadline():
            state = data.get("linked_check").get("state", CheckState.UNCHECKED)
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
                "state": state,
            }
        elif obj.is_deadline():
            state = CheckState.CHECKED if obj.flag.flag else CheckState.UNCHECKED

        data["state"] = state

        return data
