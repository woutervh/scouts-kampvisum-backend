import logging

from rest_framework import serializers

from apps.participants.models import VisumParticipant
from apps.participants.models.enums import ParticipantType, PaymentStatus
from apps.participants.serializers import InuitsParticipantSerializer


logger = logging.getLogger(__name__)


class VisumParticipantSerializer(serializers.ModelSerializer):

    participant = InuitsParticipantSerializer()
    participant_type = serializers.ChoiceField(
        choices=ParticipantType.choices, default=ParticipantType.PARTICIPANT
    )
    payment_status = serializers.ChoiceField(
        choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAYED
    )

    class Meta:
        model = VisumParticipant
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data = super().to_internal_value(data)
        return data

    def validate(self, data: dict) -> dict:
        if isinstance(data, VisumParticipant):
            return data

        return VisumParticipant(**data)
