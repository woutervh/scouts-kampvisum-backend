import logging

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.participants.models import InuitsParticipant, VisumParticipant
from apps.participants.models.enums import ParticipantType
from apps.participants.models.enums import PaymentStatus

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class VisumParticipantService:

    groupadmin = GroupAdmin()

    def create_or_update(
        self,
        user: settings.AUTH_USER_MODEL,
        participant: VisumParticipant,
        participant_type: ParticipantType = ParticipantType.PARTICIPANT,
        skip_validation: bool = False,
    ) -> VisumParticipant:
        existing_participant = VisumParticipant.objects.safe_get(id=participant.id)

        if existing_participant:
            logger.debug("Updating existing participant %s", existing_participant.id)
            return self.update_visum_participant(
                participant=existing_participant,
                updated_participant=participant,
                updated_by=user,
                skip_validation=skip_validation,
            )
        else:
            logger.debug("Creating participant %s", participant.participant.email)
            return self.create_visum_participant(
                participant=participant,
                participant_type=participant_type,
                created_by=user,
                skip_validation=skip_validation,
            )

    def create_or_update_member_participant(
        self,
        user: settings.AUTH_USER_MODEL,
        participant: VisumParticipant,
        participant_type: ParticipantType = ParticipantType.PARTICIPANT,
        instance: VisumParticipant = None,
    ) -> VisumParticipant:
        """Creates a local representation of a scouts member."""
        member_participant = None
        if participant.participant.has_group_admin_id():
            group_admin_id = participant.participant.group_admin_id
            logger.debug(
                "Looking for participant member with group admin id %s",
                group_admin_id,
            )
            member_participant = VisumParticipant.objects.safe_get(
                participant__group_admin_id=group_admin_id
            )
            scouts_member = self.groupadmin.get_member_info(
                active_user=user, group_admin_id=group_admin_id
            )

            if not scouts_member:
                raise ValidationError(
                    "Invalid group admin id for member: {}".format(group_admin_id)
                )

            member_participant = VisumParticipant()

            member_participant.participant_type = participant_type
            member_participant.participant = InuitsParticipant.from_scouts_member(
                scouts_member=scouts_member, member_participant=member_participant
            )
            member_participant.payment_status = PaymentStatus.NOT_PAYED

            member_participant.is_member = True
            member_participant.group_group_admin_id = None
            member_participant.comment = participant.comment
            member_participant.created_by = user

            member_participant.full_clean()
            member_participant.save()

        return member_participant

    def create_visum_participant(
        self,
        created_by: settings.AUTH_USER_MODEL,
        participant: VisumParticipant,
        participant_type: ParticipantType = ParticipantType.PARTICIPANT,
        skip_validation: bool = False,
    ) -> VisumParticipant:
        logger.debug("Creating VisumParticipant with email %s", participant.email)
        # Check if the instance already exists
        if participant.has_id():
            logger.debug("Querying for VisumParticipant with id %s", participant.id)
            object = VisumParticipant.objects.safe_get(pk=participant.id)
            if object:
                logger.debug(
                    "Found VisumParticipant with id %s, not creating",
                    participant.id,
                )
                return participant

        logger.debug(
            "Creating VisumParticipant with name %s %s and group admin id %s for group %s",
            participant.participant.first_name,
            participant.participant.last_name,
            participant.participant.group_admin_id,
            participant.participant.group_group_admin_id,
        )

        member = self.create_or_update_member_participant(
            participant=participant, participant_type=participant_type, user=created_by
        )
        if member:
            return member

        if not skip_validation:
            if not self.groupadmin.validate_group(
                active_user=created_by,
                group_group_admin_id=participant.group_group_admin_id,
            ):
                raise ValidationError(
                    "Invalid group admin id for group: {}".format(
                        participant.group_group_admin_id
                    )
                )

        participant = VisumParticipant(
            group_admin_id=None,
            is_member=False,
            group_group_admin_id=participant.group_group_admin_id,
            first_name=participant.first_name,
            last_name=participant.last_name,
            phone_number=participant.phone_number,
            cell_number=participant.cell_number,
            email=participant.email,
            birth_date=participant.birth_date,
            gender=participant.gender,
            street=participant.street,
            number=participant.number,
            letter_box=participant.letter_box,
            postal_code=participant.postal_code,
            city=participant.city,
            comment=participant.comment,
            created_by=created_by,
        )
        participant.full_clean()
        participant.save()

        return participant

    def update(
        self,
        *,
        participant: VisumParticipant,
        updated_participant: VisumParticipant,
        updated_by: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ) -> VisumParticipant:
        logger.debug(
            "Updating VisumParticipant with id %s and group_admin_id %s and e-mail %s",
            participant.id,
            participant.group_admin_id,
            participant.email,
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
