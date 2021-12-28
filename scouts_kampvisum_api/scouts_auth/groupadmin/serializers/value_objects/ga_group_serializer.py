import logging

from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_auth.groupadmin.serializers.value_objects import (
    AbstractScoutsLinkSerializer,
    AbstractScoutsContactSerializer,
    AbstractScoutsAddressSerializer,
    AbstractScoutsGroupSpecificFieldSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class AbstractScoutsGroupSerializer(NonModelSerializer):
    """Serializes a Group instance to a string."""

    # addresses = AbstractScoutsAddressSerializer(many=True)

    class Meta:
        model = AbstractScoutsGroup
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data: dict = {
            "group_admin_id": data.pop("id", None),
            "number": data.pop("groepsnummer", None),
            "name": data.pop("naam", None),
            "date_of_foundation": data.pop("opgericht", None),
            "bank_account": data.pop("rekeningnummer", None),
            "email": data.pop("email", None),
            "website": data.pop("website", None),
            "info": data.pop("vrijeInfo", None),
            "type": data.pop("soort", None),
            "only_leaders": bool(data.pop("enkelLeiding", None)),
            "show_members_improved": bool(data.pop("ledenVerbeterdTonen", None)),
            "addresses": AbstractScoutsAddressSerializer(many=True).to_internal_value(data.pop("adressen", [])),
            "contacts": AbstractScoutsContactSerializer(many=True).to_internal_value(data.pop("contacten", [])),
            "group_specific_fields": AbstractScoutsGroupSpecificFieldSerializer().to_internal_value(
                data.pop("groepseigenVelden", {})
            ),
            "links": AbstractScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> AbstractScoutsGroup:
        return self.create(self.validated_data)

    def create(self, validated_data) -> AbstractScoutsGroup:
        if validated_data is None:
            return None

        instance = AbstractScoutsGroup()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.number = validated_data.pop("number", None)
        instance.name = validated_data.pop("name", None)
        instance.date_of_foundation = validated_data.pop("date_of_foundation", None)
        instance.bank_account = validated_data.pop("bank_account", None)
        instance.email = validated_data.pop("email", None)
        instance.website = validated_data.pop("website", None)
        instance.info = validated_data.pop("info", None)
        instance.type = validated_data.pop("type", None)
        instance.only_leaders = validated_data.pop("only_leaders", None)
        instance.show_members_improved = validated_data.pop("show_members_improved", None)
        instance.addresses = AbstractScoutsAddressSerializer(many=True).create(validated_data.pop("addresses", []))
        instance.contacts = AbstractScoutsContactSerializer(many=True).create(validated_data.pop("contacts", []))
        instance.group_specific_fields = AbstractScoutsGroupSpecificFieldSerializer().create(
            validated_data.pop("group_specific_fields", {})
        )
        instance.links = AbstractScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
