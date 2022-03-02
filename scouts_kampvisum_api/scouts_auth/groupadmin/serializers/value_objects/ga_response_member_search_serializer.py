from scouts_auth.groupadmin.models import (
    AbstractScoutsMemberSearchMember,
    AbstractScoutsMemberSearchResponse,
)
from scouts_auth.groupadmin.serializers.value_objects import (
    AbstractScoutsLinkSerializer,
    AbstractScoutsResponseSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer

import logging

logger = logging.getLogger(__name__)


class AbstractScoutsMemberSearchMemberSerializer(NonModelSerializer):
    class Meta:
        model = AbstractScoutsMemberSearchMember
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "first_name": data.pop("voornaam", None),
            "last_name": data.pop("achternaam", None),
            "birth_date": data.pop("geboortedatum", None),
            "email": data.pop("email", None),
            "phone_number": data.pop("gsm", None),
            "links": AbstractScoutsLinkSerializer(many=True).to_internal_value(
                data.pop("links", None)
            ),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> AbstractScoutsMemberSearchMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractScoutsMemberSearchMember:
        if validated_data is None:
            return None

        instance = AbstractScoutsMemberSearchMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.first_name = validated_data.pop("first_name", None)
        instance.last_name = validated_data.pop("last_name", None)
        instance.birth_date = validated_data.pop("birth_date", None)
        instance.email = validated_data.pop("email", None)
        instance.phone_number = validated_data.pop("phone_number", None)
        instance.links = AbstractScoutsLinkSerializer(many=True).create(
            validated_data.pop("links", None)
        )

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class AbstractScoutsMemberSearchResponseSerializer(AbstractScoutsResponseSerializer):
    class Meta:
        model = AbstractScoutsMemberSearchResponse
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "members": AbstractScoutsMemberSearchMemberSerializer(
                many=True
            ).to_internal_value(data.pop("leden", [])),
        }

        validated_data = {**validated_data, **(super().to_internal_value(data))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> AbstractScoutsMemberSearchResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractScoutsMemberSearchResponse:
        if validated_data is None:
            return None

        instance = AbstractScoutsMemberSearchResponse()
        instance = super().update(instance, validated_data)

        instance.members = AbstractScoutsMemberSearchMemberSerializer(many=True).create(
            validated_data.pop("members", [])
        )

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
