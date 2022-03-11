from rest_framework import serializers

from apps.deadlines.models import DeadlineFlag


class DeadlineFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadlineFlag
        exclude = ["flag"]

    def to_internal_value(self, data: dict) -> dict:
        instance = DeadlineFlag.objects.safe_get(**data)
        if instance:
            data = {
                "id": instance.id,
                "name": instance.name,
            }

        data = super().to_internal_value(data)

        return data
