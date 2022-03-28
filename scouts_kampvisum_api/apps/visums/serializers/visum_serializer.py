from rest_framework import serializers

from apps.camps.serializers import CampSerializer, CampTypeSerializer

from apps.visums.models import CampVisum
from apps.visums.serializers import (
    LinkedCategorySetSerializer,
    CampVisumApprovalSerializer,
)

from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumSerializer(serializers.ModelSerializer):

    group = ScoutsGroupSerializer(required=False)
    camp = CampSerializer()
    camp_types = CampTypeSerializer(many=True)
    category_set = LinkedCategorySetSerializer()
    approval = CampVisumApprovalSerializer(required=False)

    class Meta:
        model = CampVisum
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data["category_set"] = {}
        data["approval"] = {}

        id = data.get("id", None)
        instance: CampVisum = CampVisum.objects.safe_get(id=id)
        if instance:
            return instance

        data = super().to_internal_value(data)
        logger.debug("DATA: %s", data)

        group = data.get("group", None)
        if not group:
            sections = data.get("camp", {}).get("sections", [])
            if sections and len(sections) > 0:
                data["group"] = sections[0].group.group_admin_id

        return data

    def to_representation(self, obj: CampVisum) -> dict:
        data = super().to_representation(obj)

        data["group_group_admin_id"] = data.get("group", {}).get("group_admin_id", None)

        return data
