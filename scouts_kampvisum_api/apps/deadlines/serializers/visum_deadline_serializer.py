import logging

from apps.deadlines.models import Deadline
from apps.deadlines.serializers import (
    DeadlineSerializer,
    LinkedSubCategoryDeadlineSerializer,
    LinkedCheckDeadlineSerializer,
    MixedDeadlineSerializer,
)

from apps.visums.models.enums import CheckState

logger = logging.getLogger(__name__)


class VisumDeadlineSerializer(DeadlineSerializer):
    class Meta:
        model = Deadline
        fields = "__all__"

    def to_representation(self, obj: Deadline) -> dict:

        if obj.parent.is_deadline():
            data = DeadlineSerializer(instance=obj).data
        elif obj.parent.is_sub_category_deadline():
            data = LinkedSubCategoryDeadlineSerializer(instance=obj).data
        elif obj.parent.is_check_deadline():
            data = LinkedCheckDeadlineSerializer(instance=obj).data
        elif obj.parent.is_mixed_deadline():
            data = MixedDeadlineSerializer(instance=obj).data
        else:
            data = super().to_representation(obj)

        sub_category_state = CheckState.CHECKED
        for sub_category in data.get("linked_sub_categories", []):
            if CheckState.is_unchecked(sub_category.get("state", CheckState.UNCHECKED)):
                sub_category_state = CheckState.UNCHECKED
                break

        check_state = CheckState.CHECKED
        for check in data.get("linked_checks", []):
            if CheckState.is_unchecked(check.get("state", CheckState.UNCHECKED)):
                check_state = CheckState.UNCHECKED
                break

        flag_state = CheckState.CHECKED
        for flag in data.get("flags", []):
            if not flag:
                flag_state = CheckState.UNCHECKED
                break

        data["state"] = (
            CheckState.CHECKED
            if sub_category_state == CheckState.CHECKED
            and check_state == CheckState.CHECKED
            and flag_state == CheckState.CHECKED
            else CheckState.UNCHECKED
        )

        return data
