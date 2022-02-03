import logging

from rest_framework import serializers

from apps.groups.models import ScoutsSectionName


logger = logging.getLogger(__name__)


class ScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSectionName object
    """

    class Meta:
        model = ScoutsSectionName
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)
        # logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)

        id = data.get("id", None)
        name = data.get("name", None)
        gender = data.get("gender", None)
        age_group = data.get("age_group", None)
        section_name = ScoutsSectionName.objects.safe_get(
            id=id, name=name, gender=gender, age_group=age_group
        )
        if section_name:
            logger.debug("DATA: %s", section_name)
            return data

        data = super().to_internal_value(data)
        # logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data

    def validate(self, data: dict) -> ScoutsSectionName:
        return ScoutsSectionName(**data)
