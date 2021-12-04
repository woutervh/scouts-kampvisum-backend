import logging

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.serializers import (
    AbstractScoutsGroupSpecificFieldSerializer,
    AbstractScoutsMemberSerializer,
)


logger = logging.getLogger(__name__)


class AbstractScoutsMemberProfileSerializer(AbstractScoutsMemberSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = super().to_internal_value(data)

        validated_data["group_specific_fields"] = AbstractScoutsGroupSpecificFieldSerializer().to_internal_value(
            data.pop("groepseigenVelden", None)
        )

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> AbstractScoutsMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractScoutsMember:
        if validated_data is None:
            return None

        instance = AbstractScoutsMember()

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
