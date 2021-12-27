import logging

from scouts_auth.groupadmin.models import AbstractScoutsGroupListResponse
from scouts_auth.groupadmin.serializers import (
    AbstractScoutsLinkSerializer,
    AbstractScoutsGroupSerializer,
    AbstractScoutsResponseSerializer,
)


logger = logging.getLogger(__name__)


class AbstractScoutsGroupListResponseSerializer(AbstractScoutsResponseSerializer):
    class Meta:
        model = AbstractScoutsGroupListResponse
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "scouts_groups": AbstractScoutsGroupSerializer(many=True).to_internal_value(data.pop("groepen", [])),
            "links": AbstractScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def create(self, validated_data: dict) -> AbstractScoutsGroupListResponse:
        if validated_data is None:
            return None

        instance = AbstractScoutsGroupListResponse()

        instance.scouts_groups = AbstractScoutsGroupSerializer(many=True).create(
            validated_data.pop("scouts_groups", [])
        )
        instance.links = AbstractScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
