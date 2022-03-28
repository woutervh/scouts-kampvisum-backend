from scouts_auth.groupadmin.models import AbstractScoutsFunctionDescriptionListResponse
from scouts_auth.groupadmin.serializers.value_objects import (
    AbstractScoutsLinkSerializer,
    AbstractScoutsFunctionDescriptionSerializer,
    AbstractScoutsResponseSerializer,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class AbstractScoutsFunctionDescriptionListResponseSerializer(
    AbstractScoutsResponseSerializer
):
    class Meta:
        model = AbstractScoutsFunctionDescriptionListResponse
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "function_descriptions": AbstractScoutsFunctionDescriptionSerializer(
                many=True
            ).to_internal_value(data.pop("functies", [])),
            "links": AbstractScoutsLinkSerializer(many=True).to_internal_value(
                data.pop("links", [])
            ),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> AbstractScoutsFunctionDescriptionListResponse:
        return self.create(self.validated_data)

    def create(
        self, validated_data: dict
    ) -> AbstractScoutsFunctionDescriptionListResponse:
        if validated_data is None:
            return None

        instance = AbstractScoutsFunctionDescriptionListResponse()

        instance.function_descriptions = AbstractScoutsFunctionDescriptionSerializer(
            many=True
        ).create(validated_data.pop("function_descriptions", []))
        instance.links = AbstractScoutsLinkSerializer(many=True).create(
            validated_data.pop("links", [])
        )

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
