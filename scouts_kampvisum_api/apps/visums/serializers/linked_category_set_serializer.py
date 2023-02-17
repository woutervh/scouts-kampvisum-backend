from rest_framework import serializers


from apps.visums.models import LinkedCategorySet
from apps.visums.models.enums import CheckState
from apps.visums.serializers import LinkedCategorySerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCategorySetSerializer(serializers.ModelSerializer):

    categories = LinkedCategorySerializer(many=True)

    class Meta:
        model = LinkedCategorySet
        exclude = ["visum"]

    def to_internal_value(self, data: dict) -> dict:
        return {}

    def to_representation(self, obj: LinkedCategorySet) -> dict:
        data = super().to_representation(obj)

        # data["state"] = CheckState.CHECKED
        # for category in data.get("categories", []):
        #     if CheckState.is_unchecked(category.get("state", CheckState.UNCHECKED)):
        #         data["state"] = CheckState.UNCHECKED
        #         break
        data["state"] = obj.check_state

        data["readable_name"] = obj.readable_name

        return data
