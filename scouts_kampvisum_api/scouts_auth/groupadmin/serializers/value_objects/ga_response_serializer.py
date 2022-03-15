from scouts_auth.groupadmin.models import AbstractScoutsResponse
from scouts_auth.groupadmin.serializers.value_objects import (
    AbstractScoutsLinkSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class AbstractScoutsResponseSerializer(NonModelSerializer):
    class Meta:
        model = AbstractScoutsResponse
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "count": data.pop("aantal", None),
            "total": data.pop("totaal", None),
            "offset": data.pop("offset", None),
            "filter_criterium": data.pop("filtercriterium", None),
            "criteria": data.pop("criteria", None),
            "links": AbstractScoutsLinkSerializer(many=True).to_internal_value(
                data.pop("links", [])
            ),
        }

        logger.debug("validated: %s", validated_data)

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> AbstractScoutsResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractScoutsResponse:
        if validated_data is None:
            return None

        instance = AbstractScoutsResponse()

        instance.count = validated_data.pop("count", None)
        instance.total = validated_data.pop("total", None)
        instance.offset = validated_data.pop("offset", None)
        instance.filter_criterium = validated_data.pop("filter_criterium", None)
        instance.criteria = validated_data.pop("criteria", None)
        instance.links = AbstractScoutsLinkSerializer(many=True).create(
            validated_data.pop("links", [])
        )

        return instance

    def update(
        self, instance: AbstractScoutsResponse, validated_data: dict
    ) -> AbstractScoutsResponse:
        instance.count = validated_data.pop("count", instance.count)
        instance.total = validated_data.pop("total", instance.total)
        instance.offset = validated_data.pop("offset", instance.offset)
        instance.filter_criterium = validated_data.pop(
            "filter_criterium", instance.filter_criterium
        )
        instance.criteria = validated_data.pop("criteria", instance.criteria)
        instance.links = validated_data.pop("links", instance.links)

        return instance
