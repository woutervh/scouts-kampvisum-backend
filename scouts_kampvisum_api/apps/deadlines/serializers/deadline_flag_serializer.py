from rest_framework import serializers

from apps.deadlines.models import DefaultDeadlineFlag


class DefaultDeadlineFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultDeadlineFlag
        exclude = ["deadline"]
