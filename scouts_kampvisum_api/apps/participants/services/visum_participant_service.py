from django.db import transaction
from django.conf import settings
from django.utils import timezone

from apps.participants.models import InuitsParticipant, VisumParticipant
from apps.participants.models.enums import ParticipantType
from apps.participants.models.enums import PaymentStatus
from apps.participants.services import InuitsParticipantService

from apps.visums.models import LinkedParticipantCheck

from scouts_auth.groupadmin.models import AbstractScoutsMember


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class VisumParticipantService:

    participant_service = InuitsParticipantService()

    @transaction.atomic
    def create_or_update_visum_participant(
        self,
        user: settings.AUTH_USER_MODEL,
        participant_type: ParticipantType = ParticipantType.PARTICIPANT,
        check: LinkedParticipantCheck = None,
        skip_validation: bool = False,
        scouts_member: AbstractScoutsMember = None,
        **fields: dict,
    ) -> VisumParticipant:
        visum_participant = VisumParticipant(**fields)
        existing_visum_participant = VisumParticipant.objects.safe_get(
            id=visum_participant.id,
            check_id=check.id,
            group_admin_id=visum_participant.participant.group_admin_id,
            inuits_participant_id=visum_participant.participant.id,
        )

        if existing_visum_participant:
            logger.debug(
                "Updating existing visum participant %s", existing_visum_participant.id
            )
            return self.update_visum_participant(
                visum_participant=existing_visum_participant,
                updated_visum_participant=visum_participant,
                updated_by=user,
                skip_validation=skip_validation,
                scouts_member=scouts_member,
            )
        else:
            logger.debug("Creating visum participant")
            return self.create_visum_participant(
                visum_participant=visum_participant,
                participant_type=participant_type,
                created_by=user,
                skip_validation=skip_validation,
                scouts_member=scouts_member,
            )

    @transaction.atomic
    def create_visum_participant(
        self,
        created_by: settings.AUTH_USER_MODEL,
        visum_participant: VisumParticipant,
        participant_type: ParticipantType = ParticipantType.PARTICIPANT,
        skip_validation: bool = False,
        scouts_member: AbstractScoutsMember = None,
    ) -> VisumParticipant:
        participant = None
        if hasattr(visum_participant, "participant"):
            participant = visum_participant.participant
        else:
            participant = InuitsParticipant(
                **visum_participant.get("participant"))

        participant = self.participant_service.create_or_update_participant(
            participant=participant,
            user=created_by,
            skip_validation=skip_validation,
            scouts_member=scouts_member,
        )

        logger.debug(
            "Creating VisumParticipant with name %s %s and group admin id %s for group %s",
            participant.first_name,
            participant.last_name,
            participant.group_admin_id,
            participant.group_group_admin_id,
        )

        visum_participant = VisumParticipant()

        visum_participant.participant_type = participant_type
        visum_participant.payment_status = visum_participant.payment_status
        visum_participant.participant = participant
        visum_participant.created_by = request.user

        visum_participant.full_clean()
        visum_participant.save()

        return visum_participant

    @transaction.atomic
    def update_visum_participant(
        self,
        *,
        visum_participant: VisumParticipant,
        updated_visum_participant: VisumParticipant,
        updated_by: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
        scouts_member: AbstractScoutsMember = None,
    ) -> VisumParticipant:
        participant = self.participant_service.create_or_update_participant(
            participant=updated_visum_participant.participant,
            user=updated_by,
            skip_validation=skip_validation,
            scouts_member=scouts_member,
        )
        logger.debug(
            "Updating VisumParticipant with id %s and group_admin_id %s and e-mail %s (for group %s)",
            visum_participant.id,
            participant.group_admin_id,
            participant.email,
            participant.group_group_admin_id,
        )

        updated_visum_participant.participant = participant

        if visum_participant.equals_visum_participant(updated_visum_participant):
            logger.debug(
                "No differences between existing VisumParticipant and updated VisumParticipant"
            )
            return visum_participant

        logger.debug("Updated: %s", updated_visum_participant)

        # Update the VisumParticipant instance
        visum_participant.participant_type = updated_visum_participant.participant_type
        visum_participant.payment_status = updated_visum_participant.payment_status
        visum_participant.participant = updated_visum_participant.participant
        visum_participant.updated_by = updated_by
        visum_participant.updated_on = timezone.now()

        visum_participant.full_clean()
        visum_participant.save()

        logger.debug("VisumParticipant instance updated (%s)",
                     visum_participant.id)

        return visum_participant

    @transaction.atomic
    def toggle_payment_status(self, request, visum_participant_id):
        participant: VisumParticipant = VisumParticipant.objects.safe_get(
            id=visum_participant_id, raise_error=True
        )

        participant.payment_status = (
            PaymentStatus.PAYED
            if participant.payment_status != PaymentStatus.PAYED
            else PaymentStatus.NOT_PAYED
        )

        participant.updated_by = request.user
        participant.updated_on = timezone.now()

        participant.full_clean()
        participant.save()

        return participant
