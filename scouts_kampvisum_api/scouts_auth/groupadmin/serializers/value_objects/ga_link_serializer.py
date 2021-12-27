import logging
from typing import List

from scouts_auth.groupadmin.models import AbstractScoutsLink

from scouts_auth.inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class AbstractScoutsLinkSectionSerializer(NonModelSerializer):
    def to_internal_value(self, data: List[str]) -> list:
        if data is None:
            return None

        return data

    def save(self) -> List[str]:
        return self.create(self.validated_data)

    def create(self, validated_data: List[str]) -> List[str]:
        if validated_data is None:
            return None

        return validated_data


class AbstractScoutsLinkSerializer(NonModelSerializer):
    class Meta:
        model = AbstractScoutsLink
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "rel": data.pop("rel", None),
            "href": data.pop("href", None),
            "method": data.pop("method", None),
            "sections": AbstractScoutsLinkSectionSerializer().to_internal_value(data.pop("secties", None)),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> AbstractScoutsLink:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractScoutsLink:
        if validated_data is None:
            return None

        instance = AbstractScoutsLink()

        instance.rel = validated_data.pop("rel", None)
        instance.href = validated_data.pop("href", None)
        instance.method = validated_data.pop("method", None)
        instance.sections = AbstractScoutsLinkSectionSerializer().create(validated_data.pop("sections", None))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
