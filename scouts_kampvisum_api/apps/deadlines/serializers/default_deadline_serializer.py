from rest_framework import serializers

from apps.camps.models import CampType
from apps.camps.serializers import CampYearSerializer, CampTypeSerializer
from apps.camps.services import CampYearService

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.serializers import (
    DeadlineDateSerializer,
    DefaultDeadlineItemSerializer,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultDeadlineSerializer(serializers.ModelSerializer):

    due_date = DeadlineDateSerializer()
    camp_year = CampYearSerializer(required=False)
    camp_types = CampTypeSerializer(many=True, required=False)
    items = DefaultDeadlineItemSerializer(many=True)

    class Meta:
        model = DefaultDeadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.trace("DEFAULT DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        camp_year = data.get("camp_year", None)
        if not camp_year:
            camp_year = CampYearService().get_or_create_current_camp_year()
            data["camp_year"] = {"id": camp_year.id, "year": camp_year.year}

        camp_types = data.get("camp_types", None)
        if not camp_types:
            default_camp_type = CampType.objects.get_default()
            default_camp_type = {
                "id": default_camp_type.id,
                "camp_type": default_camp_type.camp_type,
            }
            data["camp_types"] = [default_camp_type]

        logger.debug("DEFAULT DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data = super().to_internal_value(data)

        logger.debug("DEFAULT DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data
