import logging
from rest_framework import serializers

from apps.camps.models import CampYear

from scouts_auth.inuits.serializers.fields import (
    OptionalDateSerializerField,
    RequiredYearSerializerField,
)


logger = logging.getLogger(__name__)


class CampYearSerializer(serializers.ModelSerializer):

    year = RequiredYearSerializerField()
    start_date = OptionalDateSerializerField()
    end_date = OptionalDateSerializerField()

    class Meta:
        model = CampYear
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("CAMP YEAR SERIALIZER TO INTERNAL VALUE: %s", data)
        if isinstance(data, int):
            year = data
            data = {}
            data["year"] = year

        data = super().to_internal_value(data)

        return data

    def validate(self, data):
        # logger.debug("VALIDATING DATA: %s", data)
        if data["year"] is None:
            raise serializers.ValidationError("Year can't be null")

        return data

    def create(self, validated_data) -> CampYear:
        return CampYear(**validated_data)

    def update(self, instance, validated_data) -> CampYear:
        instance.year = validated_data.get("year", instance.year)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)

        return instance
