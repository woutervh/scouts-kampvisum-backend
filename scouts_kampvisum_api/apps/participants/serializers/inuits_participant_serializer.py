import logging

from rest_framework import serializers

from apps.participants.models import InuitsParticipant


logger = logging.getLogger(__name__)


class InuitsParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = InuitsParticipant
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("DATA: %s", data)
        # If the data dict contains an id, assume it's simple object input
        id = data.get("id", None)
        if id:
            instance = InuitsParticipant.objects.safe_get(pk=id)
            if instance:
                return instance
        data = super().to_internal_value(data)
        logger.debug("DATA: %s", data)

        return data

    def validate(self, data: dict) -> InuitsParticipant:
        return InuitsParticipant(**data)
