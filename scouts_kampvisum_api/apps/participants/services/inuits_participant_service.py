import logging

from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from apps.participants.models import InuitsParticipant

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InuitsParticipantService:

    groupadmin = GroupAdmin()

    def create_or_update_participant(
        self,
        participant: any,
        user: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ):
        if not isinstance(participant, InuitsParticipant):
            participant = InuitsParticipant(**participant)

        existing_participant = InuitsParticipant.objects.safe_get(
            id=participant.id,
            group_admin_id=participant.group_admin_id,
            email=participant.email,
        )

        if existing_participant:
            logger.debug("Updating existing participant %s", existing_participant.id)
            return self.update(
                participant=existing_participant,
                updated_participant=participant,
                updated_by=user,
                skip_validation=skip_validation,
            )
        else:
            logger.debug("Creating participant %s", participant.email)
            return self.create(
                participant=participant,
                created_by=user,
                skip_validation=skip_validation,
            )

    def create_or_update_member_participant(
        self,
        participant: InuitsParticipant,
        user: settings.AUTH_USER_MODEL,
        instance: InuitsParticipant = None,
    ) -> InuitsParticipant:
        member_participant = None
        if participant.has_group_admin_id():
            logger.debug(
                "Looking for participant member with group admin id %s",
                participant.group_admin_id,
            )
            member_participant = InuitsParticipant.objects.safe_get(
                group_admin_id=participant.group_admin_id
            )
            scouts_member = self.groupadmin.get_member_info(
                active_user=user, group_admin_id=participant.group_admin_id
            )

            if not scouts_member:
                raise ValidationError(
                    "Invalid group admin id for member: {}".format(
                        participant.group_admin_id
                    )
                )

            member_participant = InuitsParticipant.from_scouts_member(
                scouts_member, member_participant
            )

            member_participant.is_member = True
            member_participant.group_group_admin_id = None
            member_participant.comment = participant.comment
            member_participant.created_by = user

            member_participant.full_clean()
            member_participant.save()

        return member_participant

    def create(
        self,
        participant: InuitsParticipant,
        created_by: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ) -> InuitsParticipant:
        logger.debug("Creating InuitsParticipant with email %s", participant.email)
        # Check if the instance already exists
        if participant.has_id():
            logger.debug("Querying for InuitsParticipant with id %s", participant.id)
            object = InuitsParticipant.objects.safe_get(pk=participant.id)
            if object:
                logger.debug(
                    "Found InuitsParticipant with id %s, not creating",
                    participant.id,
                )
                return participant

        logger.debug(
            "Creating InuitsParticipant with name %s %s and group admin id %s for group %s",
            participant.first_name,
            participant.last_name,
            participant.group_admin_id,
            participant.group_group_admin_id,
        )

        member = self.create_or_update_member_participant(
            participant=participant, user=created_by
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

        participant = InuitsParticipant(
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
        participant: InuitsParticipant,
        updated_participant: InuitsParticipant,
        updated_by: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ) -> InuitsParticipant:
        logger.debug(
            "Updating InuitsParticipant with id %s and group_admin_id %s and e-mail %s",
            participant.id,
            participant.group_admin_id,
            participant.email,
        )
        member: InuitsParticipant = self.create_or_update_member_participant(
            participant=updated_participant, user=updated_by
        )
        if member:
            logger.debug(
                "InuitsParticipant is a scouts member, returning (%s)",
                member.group_admin_id,
            )
            return member
        logger.debug(
            "InuitsParticipant %s %s (%s) is a non-member, updating",
            participant.first_name,
            participant.last_name,
            participant.email,
        )

        if participant.equals_participant(updated_participant):
            logger.debug(
                "No differences between existing participant and updated participant"
            )
            return updated_participant

        # Update the InuitsParticipant instance
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

        logger.debug("InuitsParticipant instance updated (%s)", participant.id)

        return participant
