import logging
from rest_framework import serializers

from apps.groups.models import ScoutsSectionName

from scouts_auth.groupadmin.scouts import AgeGroup
from scouts_auth.inuits.models import Gender


logger = logging.getLogger(__name__)


class ScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSectionName object
    """

    # name = serializers.CharField(max_length=128)
    # gender = serializers.ChoiceField(choices=Gender, default=Gender.MIXED)
    # age_group = serializers.ChoiceField(
    #     choices=AgeGroup, default=AgeGroup.AGE_GROUP_UNKNOWN
    # )

    class Meta:
        model = ScoutsSectionName
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)
        logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data = super().to_internal_value(data)
        logger.debug("SECTION NAME SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data


class ScoutsSectionNameAPISerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsSectionName object for API transactions.
    """

    class Meta:
        model = ScoutsSectionName
        fields = ["name"]
