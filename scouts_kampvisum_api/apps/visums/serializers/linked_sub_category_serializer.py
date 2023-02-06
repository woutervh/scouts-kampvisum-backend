from rest_framework import serializers

from apps.visums.models import LinkedSubCategory
from apps.visums.models.enums import CheckState, CampVisumApprovalState
from apps.visums.serializers import SubCategorySerializer, LinkedCheckSerializer

from scouts_auth.inuits.serializers import PermissionRequiredSerializerField
from scouts_auth.inuits.serializers.fields import (
    OptionalCharSerializerField,
    ChoiceSerializerField,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedSubCategorySerializer(serializers.ModelSerializer):

    parent = SubCategorySerializer()
    checks = LinkedCheckSerializer(many=True)

    feedback = PermissionRequiredSerializerField(
        permission="visums.view_campvisum_feedback",
        field=OptionalCharSerializerField(),
        required=False,
    )
    approval = PermissionRequiredSerializerField(
        permission="visums.view_campvisum_approval",
        field=ChoiceSerializerField(
            choices=CampVisumApprovalState.choices,
            default=CampVisumApprovalState.UNDECIDED,
        ),
        required=False,
    )

    class Meta:
        model = LinkedSubCategory
        exclude = ["category"]

    def to_internal_value(self, data: dict) -> dict:
        pk = data.get("id", None)
        if id and len(data.keys()) == 1:
            sub_category = LinkedSubCategory.objects.safe_get(id=pk)
            if sub_category:
                return sub_category

        return super().to_internal_value(data)

    def to_representation(self, obj: LinkedSubCategory) -> dict:
        if obj.is_archived:
            return None

        data = super().to_representation(obj)

        data["state"] = CheckState.CHECKED
        for check in data.get("checks", []):
            if CheckState.is_unchecked(check.get("state", CheckState.UNCHECKED)):
                data["state"] = CheckState.UNCHECKED
                break

        data["readable_name"] = obj.readable_name

        return data
