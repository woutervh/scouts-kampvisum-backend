from rest_framework import serializers

from apps.visums.models import LinkedCheck
from apps.visums.serializers import CheckSerializer


class LinkedCheckSerializer(serializers.ModelSerializer):

    parent = CheckSerializer()

    class Meta:
        model = LinkedCheck
        exclude = ["sub_category"]
