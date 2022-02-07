import logging

from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.camps.models import Camp
from apps.camps.serializers import CampYearSerializer
from apps.camps.services import CampYearService

from apps.groups.serializers import ScoutsSectionSerializer


logger = logging.getLogger(__name__)


class CampSerializer(serializers.ModelSerializer):
    """
    Serializes a Camp instance from and to the frontend.
    """

    year = CampYearSerializer()
    sections = ScoutsSectionSerializer(many=True)
    # sections = serializers.PrimaryKeyRelatedField(
    #     queryset=ScoutsSection.objects.all(), many=True
    # )

    class Meta:
        model = Camp
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("CAMP SERIALIZER TO_INTERNAL_VALUE: %s", data)
        year = data.get("year", None)
        if not year:
            year = CampYearService().get_or_create_current_camp_year()
            data["year"] = year.year

        data = super().to_internal_value(data)
        # logger.debug("CAMP SERIALIZER TO INTERNAL VALUE: %s", data)

        return data

    def validate(self, data: dict) -> dict:
        # logger.debug("CAMP SERIALIZER VALIDATE: %s", data)

        if not data.get("name"):
            raise ValidationError("A Camp must have a name")

        if not data.get("sections"):
            raise ValidationError("A Camp must have at least 1 Section attached")

        return data

    def create(self, validated_data) -> Camp:
        return Camp(**validated_data)

    def update(self, instance, validated_data) -> Camp:
        instance.name = validated_data.get("type", instance.type)
        instance.year = CampYearSerializer(null=True)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.sections = ScoutsSectionSerializer(many=True)

        return instance
