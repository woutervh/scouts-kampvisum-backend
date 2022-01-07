from rest_framework import serializers

from apps.visums.models import VisumCheck
from apps.visums.serializers import SubCategorySerializer, CheckTypeSerializer


class VisumCheckSerializer(serializers.ModelSerializer):

    sub_category = SubCategorySerializer()
    check_type = CheckTypeSerializer()

    class Meta:
        model = VisumCheck
        fields = "__all__"
