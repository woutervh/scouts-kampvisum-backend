import logging
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from ..models import Camp
from apps.groups.api.models import Section
from apps.groups.api.serializers import (
    SectionAPISerializer
)
from inuits.serializers.fields import OptionalDateField, RequiredYearField


logger = logging.getLogger(__name__)


class CampAPISerializer(serializers.ModelSerializer):
    """
    Deserializes a JSON Camp from the frontend (no serialization).
    """

    year = RequiredYearField()
    name = serializers.CharField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()
    # List of Section uuid's
    sections = SectionAPISerializer()

    class Meta:
        model = Camp
        fields = '__all__'

    def validate(self, data):
        logger.debug('Camp API DATA: %s', data)

        if not data.get('name'):
            raise ValidationError(
                "A Camp must have a name")

        if not data.get('sections'):
            raise ValidationError(
                "A Camp must have at least 1 Section attached"
            )
        else:
            for section_uuid in data.get('sections'):
                try:
                    Section.objects.get(uuid=section_uuid)
                except ObjectDoesNotExist:
                    raise ValidationError(
                        "Invalid UUID. No Section with that UUID: " +
                        str(section_uuid)
                    )

        # if data.get('start_date') and data.get('start_date') < timezone.now():
        #     raise ValidationError("The camp start date can't be in the past")

        return data
