from rest_framework import serializers

from apps.deadlines.models import DefaultDeadlineItem
from apps.deadlines.serializers import DefaultDeadlineFlagSerializer

from apps.visums.serializers import SubCategorySerializer, CheckSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultDeadlineItemSerializer(serializers.ModelSerializer):

    item_flag = DefaultDeadlineFlagSerializer(required=False)
    item_sub_category = SubCategorySerializer(required=False)
    item_check = CheckSerializer(required=False)

    class Meta:
        model = DefaultDeadlineItem
        fields = "__all__"
