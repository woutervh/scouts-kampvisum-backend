import logging
from typing import List

from scouts_auth.groupadmin.models import AbstractScoutsGroupSpecificField

from scouts_auth.inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class AbstractScoutsGroupSpecificFieldSerializer(NonModelSerializer):
    class Meta:
        model = AbstractScoutsGroupSpecificField
        abstract = True

    def to_internal_value(self, data: dict) -> list:
        if data is None:
            return None

        validated_data = []
        groups = data.keys()

        for group in groups:
            group_data: dict = data.get(group, None)
            validated = {}

            validated["scouts_group"] = group
            validated["schema"] = group_data.pop("schema", None)
            # validated["values"] = AbstractScoutsValueSerializer().to_internal_value(group_data.pop("waarden", {}))

            validated_data.append(validated)

        return validated_data

    def save(self) -> AbstractScoutsGroupSpecificField:
        return self.create(self.validated_data)

    def create(self, validated_data: list) -> List[AbstractScoutsGroupSpecificField]:
        if validated_data is None:
            return None

        fields = []
        for data in validated_data:
            instance = AbstractScoutsGroupSpecificField()

            instance.scouts_group = data.pop("scouts_group", None)
            instance.schema = data.pop("schema", None)
            # instance.values = AbstractScoutsValueSerializer().create(data.pop("values", {}))

            fields.append(instance)

        return fields
