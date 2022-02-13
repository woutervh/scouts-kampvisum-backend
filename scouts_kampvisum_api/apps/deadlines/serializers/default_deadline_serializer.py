import logging

from rest_framework import serializers

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.serializers import (
    DeadlineDateSerializer,
    DefaultDeadlineFlagSerializer,
)

from apps.visums.serializers import SubCategorySerializer, CheckSerializer


logger = logging.getLogger(__name__)


class DefaultDeadlineSerializer(serializers.ModelSerializer):

    due_date = DeadlineDateSerializer()
    sub_categories = SubCategorySerializer(many=True, required=False)
    checks = CheckSerializer(many=True, required=False)
    flags = DefaultDeadlineFlagSerializer(many=True, required=False)

    class Meta:
        model = DefaultDeadline
        fields = "__all__"
