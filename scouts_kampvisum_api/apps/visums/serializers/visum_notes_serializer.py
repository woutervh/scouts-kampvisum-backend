from rest_framework import serializers

from apps.visums.models import CampVisum

from scouts_auth.inuits.serializers import PermissionRequiredSerializerField
from scouts_auth.inuits.serializers.fields import OptionalCharSerializerField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumNotesSerializer(serializers.ModelSerializer):

    notes = PermissionRequiredSerializerField(
        permission="visums.edit_visum_notes",
        field=OptionalCharSerializerField(),
        required=True,
    )

    class Meta:
        model = CampVisum
        fields = ["notes"]
