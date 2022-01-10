from rest_framework import serializers

from apps.visums.models import Check
from apps.visums.serializers import SubCategorySerializer, CheckTypeSerializer


class CheckSerializer(serializers.ModelSerializer):

    # sub_category = SubCategorySerializer()
    check_type = CheckTypeSerializer()

    class Meta:
        model = Check
        # fields = "__all__"
        exclude = ["sub_category"]
