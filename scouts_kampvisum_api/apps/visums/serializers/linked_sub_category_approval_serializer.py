from rest_framework import serializers

from apps.visums.models import LinkedSubCategory
from apps.visums.models.enums import CampVisumApprovalState

from scouts_auth.inuits.serializers import PermissionRequiredSerializerField
from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedSubCategoryApprovalSerializer(serializers.ModelSerializer):

    approval = PermissionRequiredSerializerField(
        permission="visums.change_campvisum_approval",
        field=ChoiceSerializerField(
            choices=CampVisumApprovalState.choices,
            default=CampVisumApprovalState.UNDECIDED,
        ),
        required=True,
    )

    class Meta:
        model = LinkedSubCategory
        fields = ["approval"]
