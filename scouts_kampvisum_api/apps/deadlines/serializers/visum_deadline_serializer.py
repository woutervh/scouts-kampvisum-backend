import logging

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.serializers import (
    DeadlineSerializer,
    LinkedSubCategoryDeadlineSerializer,
    LinkedCheckDeadlineSerializer,
)


logger = logging.getLogger(__name__)


class VisumDeadlineSerializer(DeadlineSerializer):
    class Meta:
        model = DefaultDeadline
        fields = "__all__"

    def to_representation(self, obj: DefaultDeadline) -> dict:

        if obj.is_deadline():
            return DeadlineSerializer(instance=obj).data

        if obj.is_sub_category_deadline():
            return LinkedSubCategoryDeadlineSerializer(instance=obj).data

        if obj.is_check_deadline():
            return LinkedCheckDeadlineSerializer(instance=obj).data

        return super().to_representation(obj)
