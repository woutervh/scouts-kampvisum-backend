import logging

from django.db import transaction
from django.conf import settings

from apps.participants.models import VisumParticipant
from apps.participants.models.enums import ParticipantType
from apps.participants.models.enums import PaymentStatus
from apps.participants.services import InuitsParticipantService


logger = logging.getLogger(__name__)


class VisumParticipantService:

    participant_service = InuitsParticipantService()

    @transaction.atomic
    def create_or_update(
        self,
        user: settings.AUTH_USER_MODEL,
        participant_type: ParticipantType = ParticipantType.PARTICIPANT,
        skip_validation: bool = False,
        **fields: dict,
    ) -> VisumParticipant:
        visum_participant = VisumParticipant(**fields)
        existing_visum_participant = VisumParticipant.objects.safe_get(
            id=fields.get("id", None)
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
            )
        else:
            logger.debug(
                "Creating visum participant %s", visum_participant.participant.email
            )
            return self.create_visum_participant(
                visum_participant=visum_participant,
                participant_type=participant_type,
                created_by=user,
                skip_validation=skip_validation,
            )

    @transaction.atomic
    def create_visum_participant(
        self,
        created_by: settings.AUTH_USER_MODEL,
        visum_participant: VisumParticipant,
        participant_type: ParticipantType = ParticipantType.PARTICIPANT,
        skip_validation: bool = False,
    ) -> VisumParticipant:
        logger.debug(
            "Creating VisumParticipant with email %s",
            visum_participant.participant.email,
        )
        # Check if the instance already exists
        if visum_participant.has_id():
            logger.debug(
                "Querying for VisumParticipant with id %s", visum_participant.id
            )
            object = VisumParticipant.objects.safe_get(pk=visum_participant.id)
            if object:
                logger.debug(
                    "Found VisumParticipant with id %s, not creating",
                    visum_participant.id,
                )
                return visum_participant

        logger.debug(
            "Creating VisumParticipant with name %s %s and group admin id %s for group %s",
            visum_participant.participant.first_name,
            visum_participant.participant.last_name,
            visum_participant.participant.group_admin_id,
            visum_participant.participant.group_group_admin_id,
        )

        participant = self.participant_service.create_or_update(
            participant=visum_participant.participant,
            user=created_by,
            skip_validation=skip_validation,
        )

        visum_participant = VisumParticipant()

        visum_participant.participant_type = participant_type
        visum_participant.payment_status = visum_participant.payment_status
        visum_participant.participant = participant

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
    ) -> VisumParticipant:
        logger.debug(
            "Updating VisumParticipant with id %s and group_admin_id %s and e-mail %s",
            visum_participant.id,
            visum_participant.group_admin_id,
            visum_participant.email,
        )
        member = self.create_or_update_member_participant(
            participant=updated_participant, user=updated_by
        )
        if member:
            return member

        if participant.equals_participant(updated_participant):
            logger.debug(
                "No differences between existing participant and updated participant"
            )
            return updated_participant

        logger.debug("Updated: %s", updated_participant)

        # Update the VisumParticipant instance
        participant.group_group_admin_id = (
            updated_participant.group_group_admin_id
            if updated_participant.group_group_admin_id
            else participant.group_group_admin_id
        )
        participant.first_name = (
            updated_participant.first_name
            if updated_participant.first_name
            else participant.first_name
        )
        participant.last_name = (
            updated_participant.last_name
            if updated_participant.last_name
            else participant.last_name
        )
        participant.phone_number = (
            updated_participant.phone_number
            if updated_participant.phone_number
            else participant.phone_number
        )
        participant.cell_number = (
            updated_participant.cell_number
            if updated_participant.cell_number
            else participant.cell_number
        )
        participant.email = (
            updated_participant.email
            if updated_participant.email
            else participant.email
        )
        participant.birth_date = (
            updated_participant.birth_date
            if updated_participant.birth_date
            else participant.birth_date
        )
        participant.gender = (
            updated_participant.gender
            if updated_participant.gender
            else participant.gender
        )
        participant.street = (
            updated_participant.street
            if updated_participant.street
            else participant.street
        )
        participant.number = (
            updated_participant.number
            if updated_participant.number
            else participant.number
        )
        participant.letter_box = (
            updated_participant.letter_box
            if updated_participant.letter_box
            else participant.letter_box
        )
        participant.postal_code = (
            updated_participant.postal_code
            if updated_participant.postal_code
            else participant.postal_code
        )
        participant.city = (
            updated_participant.city if updated_participant.city else participant.city
        )
        participant.comment = (
            updated_participant.comment
            if updated_participant.comment
            else participant.comment
        )
        participant.updated_by = updated_by

        participant.full_clean()
        participant.save()

        logger.debug("VisumParticipant instance updated (%s)", participant.id)

        return participant

    @transaction.atomic
    def toggle_payment_status(self, participant_id):
        participant: VisumParticipant = VisumParticipant.objects.safe_get(
            id=participant_id, raise_error=True
        )

        participant.payment_status = (
            PaymentStatus.PAYED
            if participant.payment_status != PaymentStatus.PAYED
            else PaymentStatus.NOT_PAYED
        )

        participant.full_clean()
        participant.save()

        return participant
