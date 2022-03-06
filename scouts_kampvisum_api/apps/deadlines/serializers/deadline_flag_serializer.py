from rest_framework import serializers

from apps.deadlines.models import DeadlineFlag
from apps.deadlines.serializers import DefaultDeadlineFlagSerializer


class DeadlineFlagSerializer(serializers.ModelSerializer):

    parent = DefaultDeadlineFlagSerializer()

    class Meta:
        model = DeadlineFlag
        fields = "__all__"
