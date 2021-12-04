import logging

from scouts_auth.groupadmin.models import (
    AbstractAbstractScoutsMemberListMember,
    AbstractAbstractScoutsMemberListResponse,
)
from scouts_auth.groupadmin.serializers import (
    AbstractScoutsValueSerializer,
    AbstractScoutsLinkSerializer,
    AbstractScoutsResponseSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class AbstractAbstractScoutsMemberListMemberSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "index": data.pop("positie", None),
            "values": AbstractScoutsValueSerializer(many=True).to_internal_value(
                list(data.pop("waarden", {}).items())
            ),
            "links": AbstractScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> AbstractAbstractScoutsMemberListMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractAbstractScoutsMemberListMember:
        if validated_data is None:
            return None

        instance = AbstractAbstractScoutsMemberListMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.index = validated_data.pop("index", None)
        instance.values = AbstractScoutsValueSerializer(many=True).create(validated_data.pop("values", {}))
        instance.links = AbstractScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class AbstractAbstractScoutsMemberListResponseSerializer(AbstractScoutsResponseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "members": AbstractAbstractScoutsMemberListMemberSerializer(many=True).to_internal_value(
                data.pop("leden", [])
            ),
        }

        validated_data = {**validated_data, **(super().to_internal_value(data))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> AbstractAbstractScoutsMemberListResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractAbstractScoutsMemberListResponse:
        if validated_data is None:
            return None

        instance = AbstractAbstractScoutsMemberListResponse()

        instance.members = AbstractAbstractScoutsMemberListMemberSerializer(many=True).create(
            validated_data.pop("members", [])
        )

        super().create(validated_data)

        logger.debug("INSTANCE: %s", instance)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
