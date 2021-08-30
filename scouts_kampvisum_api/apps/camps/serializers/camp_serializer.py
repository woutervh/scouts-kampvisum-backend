import logging
from rest_framework import serializers

from ..models import Camp
from ..serializers import CampYearSerializer
from apps.groups.api.serializers import SectionSerializer
from inuits.mixins import FlattenMixin
from inuits.serializers.fields import OptionalDateField


logger = logging.getLogger(__name__)


class CampSerializer(FlattenMixin, serializers.ModelSerializer):
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
        fields = ('name', 'year', 'start_date', 'end_date', 'sections')
        flatten = [('year', CampYearSerializer)]

    def create(self, validated_data) -> Camp:
        return Camp(**validated_data)

    def update(self, instance, validated_data) -> Camp:
        instance.name = validated_data.get(
            'type', instance.type)
        instance.year = CampYearSerializer(null=True)
        instance.start_date = validated_data.get(
            'start_date', instance.start_date)
        instance.end_date = validated_data.get(
            'end_date', instance.end_date)
        instance.sections = SectionSerializer(many=True)

        return instance
