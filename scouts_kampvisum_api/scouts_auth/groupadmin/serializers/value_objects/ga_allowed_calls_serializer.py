from scouts_auth.groupadmin.models import ScoutsAllowedCalls
from scouts_auth.groupadmin.serializers.value_objects import (
    AbstractScoutsLinkSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsAllowedCallsSerializer(NonModelSerializer):
    class Meta:
        model = ScoutsAllowedCalls
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "links": AbstractScoutsLinkSerializer(many=True).to_internal_value(
                data.pop("links", [])
            )
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsAllowedCalls:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsAllowedCalls:
        if validated_data is None:
            return None

        instance = ScoutsAllowedCalls()

        instance.links = AbstractScoutsLinkSerializer(many=True).create(
            validated_data.pop("links", [])
        )

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
