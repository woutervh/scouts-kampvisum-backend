import logging
from rest_framework import serializers

from ..models import CampYear
from inuits.serializers.fields import RequiredYearField


logger = logging.getLogger(__name__)


class CampYearAPISerializer(serializers.Serializer):

    year = RequiredYearField()

    class Meta:
        model = CampYear
        fields = '__all__'

    def validate(self, data):
        logger.debug("VALIDATING DATA: %s", data)
        if data['year'] is None:
            raise serializers.ValidationError("Year can't be null")

        return data
