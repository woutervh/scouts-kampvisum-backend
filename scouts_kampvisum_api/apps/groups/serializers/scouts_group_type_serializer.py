from rest_framework import serializers

from apps.groups.models import ScoutsGroupType


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroupTypeSerializer(serializers.ModelSerializer):
    """
    Serializes a GroupType object.
    """

    # parent = RecursiveSerializerField(null=True, blank=True)

    class Meta:
        model = ScoutsGroupType
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("GROUP TYPE TO_INTERNAL_VALUE: %s", data)

        parent = data.get("parent", None)
        if parent:
            data["parent"] = {"group_type": parent}

        # logger.debug("GROUP TYPE TO_INTERNAL_VALUE: %s", data)

        data = super().to_internal_value(data)

        # logger.debug("GROUP TYPE TO_INTERNAL_VALUE: %s", data)

        return data
