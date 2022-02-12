from rest_framework import serializers

from apps.deadlines.models import DeadlineFlag


class DeadlineFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadlineFlag
        exclude = ["deadline"]
