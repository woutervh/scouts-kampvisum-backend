import logging

from scouts_auth.groupadmin.models import AbstractScoutsFunctionListResponse
from scouts_auth.groupadmin.serializers.value_objects import (
    AbstractScoutsLinkSerializer,
    AbstractScoutsFunctionSerializer,
    AbstractScoutsResponseSerializer,
)


logger = logging.getLogger(__name__)


class AbstractScoutsFunctionListResponseSerializer(AbstractScoutsResponseSerializer):
    class Meta:
        model = AbstractScoutsFunctionListResponse
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "functions": AbstractScoutsFunctionSerializer(many=True).to_internal_value(data.pop("functies", [])),
            "links": AbstractScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> AbstractScoutsFunctionListResponse:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractScoutsFunctionListResponse:
        if validated_data is None:
            return None

        instance = AbstractScoutsFunctionListResponse()

        instance.functions = AbstractScoutsFunctionSerializer(many=True).create(validated_data.pop("functions", []))
        instance.links = AbstractScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
