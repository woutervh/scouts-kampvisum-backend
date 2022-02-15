import logging

from rest_framework import serializers

from apps.camps.serializers import CampSerializer
from apps.visums.models import CampVisum
from apps.visums.serializers import LinkedCategorySetSerializer


logger = logging.getLogger(__name__)


class CampVisumSerializer(serializers.ModelSerializer):

    camp = CampSerializer()
    category_set = LinkedCategorySetSerializer()

    class Meta:
        model = CampVisum
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("VISUM SERIALIZER TO INTERNAL VALUE: %s", data)

        data["category_set"] = {}
        camp_types = data.pop("camp_types", [])

        data = super().to_internal_value(data)

        data["camp_types"] = camp_types

        return data

    def to_representation(self, data: dict) -> dict:
        # logger.debug("VISUM SERIALIZER TO REPRESENTATION: %s", data)

        data = super().to_representation(data)

        data["group_group_admin_id"] = (
            data.get("camp", {}).get("sections", [])[0].get("group_admin_id", None)
        )
        # logger.debug("VISUM SERIALIZER TO REPRESENTATION: %s", data)

        return data
