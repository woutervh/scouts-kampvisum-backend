from rest_framework import serializers

from apps.camps.serializers import CampSerializer, CampTypeSerializer
from apps.visums.models import CampVisum
from apps.visums.serializers import LinkedCategorySetSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumSerializer(serializers.ModelSerializer):

    camp = CampSerializer()
    camp_types = CampTypeSerializer(many=True)
    category_set = LinkedCategorySetSerializer()

    class Meta:
        model = CampVisum
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data["category_set"] = {}

        id = data.get("id", None)
        instance: CampVisum = CampVisum.objects.safe_get(id=id)
        if instance:
            return instance

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: CampVisum) -> dict:
        data = super().to_representation(obj)

        data["group_group_admin_id"] = (
            data.get("camp", {})
            .get("sections", [])[0]
            .get("group_group_admin_id", None)
        )

        return data
