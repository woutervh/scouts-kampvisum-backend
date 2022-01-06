import logging

from rest_framework import serializers

from apps.camps.models import Camp
from apps.camps.serializers import CampYearSerializer
from apps.groups.serializers import ScoutsSectionSerializer

from scouts_auth.inuits.mixins import FlattenSerializerMixin


logger = logging.getLogger(__name__)


class CampSerializer(FlattenSerializerMixin, serializers.ModelSerializer):
    """
    Serializes a Camp object.
    """

    # name = serializers.CharField()
    # year = CampYearSerializer()
    # start_date = OptionalDateField()
    # end_date = OptionalDateField()
    # sections = SectionSerializer(many=True)

    class Meta:
        model = Camp
        fields = ("name", "year", "start_date", "end_date", "sections")
        flatten = [("year", CampYearSerializer)]

    def create(self, validated_data) -> Camp:
        return Camp(**validated_data)

    def update(self, instance, validated_data) -> Camp:
        instance.name = validated_data.get("type", instance.type)
        instance.year = CampYearSerializer(null=True)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.sections = ScoutsSectionSerializer(many=True)

        return instance
