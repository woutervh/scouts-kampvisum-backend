import logging

from apps.deadlines.models import Deadline
from apps.deadlines.serializers import (
    DeadlineSerializer,
    LinkedSubCategoryDeadlineSerializer,
    LinkedCheckDeadlineSerializer,
    MixedDeadlineSerializer,
)


logger = logging.getLogger(__name__)


class VisumDeadlineSerializer(DeadlineSerializer):
    class Meta:
        model = Deadline
        fields = "__all__"

    def to_representation(self, obj: Deadline) -> dict:

        if obj.parent.is_deadline():
            return DeadlineSerializer(instance=obj).data

        if obj.parent.is_sub_category_deadline():
            return LinkedSubCategoryDeadlineSerializer(instance=obj).data

        if obj.parent.is_check_deadline():
            return LinkedCheckDeadlineSerializer(instance=obj).data

        if obj.parent.is_mixed_deadline():
            return MixedDeadlineSerializer(instance=obj).data

        return super().to_representation(obj)
