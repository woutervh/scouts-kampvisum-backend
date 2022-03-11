from rest_framework import serializers

from apps.deadlines.models import LinkedDeadlineFlag
from apps.deadlines.serializers import DeadlineFlagSerializer


class LinkedDeadlineFlagSerializer(serializers.ModelSerializer):

    parent = DeadlineFlagSerializer()

    class Meta:
        model = LinkedDeadlineFlag
        fields = "__all__"
