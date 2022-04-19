from rest_framework import serializers

from apps.visums.models import LinkedSubCategory
from apps.visums.models.enums import CheckState
from apps.visums.serializers import SubCategorySerializer, LinkedCheckSerializer

from scouts_auth.inuits.serializers import PermissionRequiredSerializerField
from scouts_auth.inuits.serializers.fields import (
    OptionalCharSerializerField,
    DefaultCharSerializerField,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedSubCategoryFeedbackSerializer(serializers.ModelSerializer):

    feedback = PermissionRequiredSerializerField(
        permission="visums.edit_visum_feedback",
        field=OptionalCharSerializerField(),
        required=True,
    )

    class Meta:
        model = LinkedSubCategory
        fields = ["feedback"]
