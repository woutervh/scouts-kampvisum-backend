from rest_framework import serializers

from apps.camps.models import CampYear

from scouts_auth.inuits.serializers.fields import (
    OptionalDateSerializerField,
    RequiredYearSerializerField,
)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


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

    def validate(self, data) -> CampYear:
        # Safe to raise an error, because this serializer will not be used to create a CampType
        return CampYear.objects.safe_get(
            id=data.get("id", None),
            year=data.get("year", None),
            start_date=data.get("start_date", None),
            end_date=data.get("end_date", None),
            raise_error=True,
        )

    def create(self, validated_data) -> CampYear:
        return CampYear(**validated_data)

    def update(self, instance, validated_data) -> CampYear:
        instance.year = validated_data.get("year", instance.year)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)

        return instance
