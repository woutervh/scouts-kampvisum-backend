import logging
from rest_framework import serializers

from ..models import CampYear
from inuits.serializers.fields import RequiredYearField


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
