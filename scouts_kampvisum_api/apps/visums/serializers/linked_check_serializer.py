from rest_framework import serializers

from apps.visums.models import LinkedCheck
from apps.visums.serializers import LinkedSubCategorySerializer, CheckSerializer


class LinkedCheckSerializer(serializers.ModelSerializer):

    parent = CheckSerializer()
    sub_category = LinkedSubCategorySerializer()

    class Meta:
        model = LinkedCheck
        fields = "__all__"
