from django.db import models

from apps.participants.models import InuitsParticipant
from apps.participants.models.enums import ParticipantType, PaymentStatus
from apps.participants.managers import VisumParticipantManager

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import DefaultCharField


class VisumParticipant(AuditedBaseModel):
    objects = VisumParticipantManager()

    participant = models.OneToOneField(
        InuitsParticipant, on_delete=models.CASCADE, related_name="visum_participant"
    )
    participant_type = DefaultCharField(
        choices=ParticipantType.choices,
        default=ParticipantType.PARTICIPANT,
        max_length=1,
    )
    payment_status = DefaultCharField(
        choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAYED, max_length=1
    )

    class Meta:
        ordering = [
            "participant__first_name",
            "participant__last_name",
            "participant__birth_date",
            "participant__group_group_admin_id",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def equals_visum_participant(self, updated_visum_participant):
        if updated_visum_participant is None:
            return False

        if (
            not type(updated_visum_participant).__class__.__name__
            == self.__class__.__name__
        ):
            return False

        return (
            self.equals_participant(updated_visum_participant.participant)
            and self.participant_type == updated_visum_participant.participant_type
            and self.payment_status == updated_visum_participant.payment_status
        )

    def __str__(self):
        return "id ({}), participant_type ({}), payment_status ({}), participant({})".format(
            self.id, self.participant_type, self.payment_status, str(self.participant)
        )
