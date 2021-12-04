import logging
from rest_framework import serializers

from apps.camps.models import CampYear

from scouts_auth.inuits.serializers.fields import OptionalDateField, RequiredYearField


logger = logging.getLogger(__name__)


class CampYearAPISerializer(serializers.Serializer):
    class Meta:
        model = CampYear
        fields = ["year"]

    def validate(self, data):
        logger.debug("VALIDATING DATA: %s", data)
        if data["year"] is None:
            raise serializers.ValidationError("Year can't be null")

        return data


class CampYearSerializer(serializers.ModelSerializer):

    year = RequiredYearField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()

    class Meta:
        model = CampYear
        fields = "__all__"

    def create(self, validated_data) -> CampYear:
        return CampYear(**validated_data)

    def update(self, instance, validated_data) -> CampYear:
        instance.year = validated_data.get("year", instance.year)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)

        return instance
