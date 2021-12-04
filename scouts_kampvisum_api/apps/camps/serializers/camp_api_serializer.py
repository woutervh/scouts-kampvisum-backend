import logging
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from apps.camps.models import Camp
from apps.camps.serializers import CampYearAPISerializer

from apps.groups.models import ScoutsSection
from apps.groups.serializers import ScoutsSectionAPISerializer

from scouts_auth.inuits.mixins import FlattenSerializerMixin


logger = logging.getLogger(__name__)


class CampAPISerializer(FlattenSerializerMixin, serializers.ModelSerializer):
    """
    Serializes a Camp instance from and to the frontend.
    """

    sections = ScoutsSectionAPISerializer(many=True)

    class Meta:
        model = Camp
        fields = ("name", "start_date", "end_date", "sections")
        flatten = [("year", CampYearAPISerializer)]

    def validate(self, data):
        logger.debug("Camp API DATA: %s", data)

        if not data.get("name"):
            raise ValidationError("A Camp must have a name")

        if not data.get("year"):
            raise ValidationError("A camp must be tied to a CampYear")

        if not data.get("sections"):
            raise ValidationError("A Camp must have at least 1 Section attached")
        else:
            for section_uuid in data.get("sections"):
                try:
                    ScoutsSection.objects.get(uuid=section_uuid)
                except ObjectDoesNotExist:
                    raise ValidationError(
                        "Invalid UUID. No Section with that UUID: " + str(section_uuid)
                    )

        return data
