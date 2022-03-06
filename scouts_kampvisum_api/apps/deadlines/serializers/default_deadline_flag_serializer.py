from rest_framework import serializers

from apps.deadlines.models import DefaultDeadlineFlag


class DefaultDeadlineFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultDeadlineFlag
        exclude = ["flag"]

    def to_internal_value(self, data: dict) -> dict:
        instance = DefaultDeadlineFlag.objects.safe_get(**data)
        if instance:
            data = {
                "id": instance.id,
                "name": instance.name,
            }

        data = super().to_internal_value(data)

        return data
