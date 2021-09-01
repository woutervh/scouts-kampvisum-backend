import logging
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from ..models import Camp
from ..serializers import CampYearAPISerializer
from apps.groups.api.models import Section
from apps.groups.api.serializers import (
    SectionAPISerializer,
    CampVisumSectionAPISerializer,
)
from inuits.mixins import FlattenMixin
from inuits.serializers.fields import OptionalDateField


logger = logging.getLogger(__name__)


# @see https://stackoverflow.com/a/33413886
# try:
#     from apps.visums.api.serializers import CampVisumSerializer
# except ImportError:
#     import sys
#     logger.debug('sys: %s', sys.modules)
#     package = 'apps.visums.api.serializers'
#     CampVisumSerializer = sys.modules[package + '.CampVisumSerializer']
# CampVisumSerializer = sys.modules[__package__ + '.CampVisumSerializer']


class CampAPISerializer(FlattenMixin, serializers.ModelSerializer):
    """
    Serializes a Camp instance from and to the frontend.
    """

    sections = SectionAPISerializer(many=True)

    class Meta:
        model = Camp
        fields = ("uuid", "name", "start_date", "end_date", "sections")
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
                    Section.objects.get(uuid=section_uuid)
                except ObjectDoesNotExist:
                    raise ValidationError(
                        "Invalid UUID. No Section with that UUID: " + str(section_uuid)
                    )

        return data
